"""Phase 40 / TRAIN-01 -- CurriculumController tests.

Dataset-free (stub source/model only). Exercises the outer curriculum loop's
ADVANCE/RECOVER/HALT dispatch primarily via the forced-disposition injection
seam (fast, isolated dispatch tests) plus the T-40-09 construction guard, the
cycle-2 H3 cold-start RECOVER backstop, and the CTX-38/45 run-start logging
and anchor-ordering contracts. A single dedicated test exercises the
composed, gate-earned ADVANCE path through a REAL (non-forced) RunController
with test-local permissive thresholds -- proving the production-of-ADVANCE
path, not only the dispatch-of-ADVANCE path.
"""

from __future__ import annotations

import importlib
import inspect
import tempfile
import unittest
from unittest import mock

import numpy as np
import torch

from tests.phase40 import _SKIP_PHRASE
from tests.phase40._fixtures import (
    make_stub_model,
    make_stub_source,
    make_stub_split_sources,
)
from pinn.loss_catalog import LossTerms

MODULE = "pinn.training.controllers"


def _require(symbol):
    try:
        mod = importlib.import_module(MODULE)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {MODULE}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {MODULE}.{symbol}")
    return getattr(mod, symbol)


from pinn.runtime import resolve_runtime  # noqa: E402
from pinn.training.checkpoint import TorchSaveCheckpointStore  # noqa: E402
from pinn.training.collocation_sampler import CollocationSampler  # noqa: E402
from pinn.training.config import OptConfig, StageConfig, TrainingConfig  # noqa: E402
from pinn.training.grad_clip import GradClipper  # noqa: E402
from pinn.training.scheduled_weights import ScheduledWeights  # noqa: E402
from pinn.training.slbfgs_preflight import StochasticLBFGSNotImplemented  # noqa: E402
from pinn.training.stage_exit import StageDisposition, StageExitMachine  # noqa: E402


# ---------------------------------------------------------------------------
# Shared test helpers.
# ---------------------------------------------------------------------------

def _make_config(*, max_epochs=1, n_adam=1, validation_every=10_000, lbfgs_chunk_size=4,
                 lbfgs_max_iter=2, **stage_overrides):
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
    stage = StageConfig(**stage_kwargs)
    opt = OptConfig(
        validation_every=validation_every,
        lbfgs_chunk_size=lbfgs_chunk_size,
        lbfgs_max_iter=lbfgs_max_iter,
    )
    return TrainingConfig(stage=stage, opt=opt)


def _minimal_controller(tmp_dir, *, forced_disposition=None, run_controller=None,
                        recover_retries=0, config=None, initial_stage=0):
    """Build a CurriculumController with a real TorchSaveCheckpointStore.

    ``config``/``scheduled_weights`` are cheap, real objects (no stubbing
    needed -- they are pure-python/no-tensor state machines); only the
    disposition SOURCE (``run_controller`` xor ``forced_disposition``) is
    swappable per test.
    """
    CurriculumController = _require("CurriculumController")
    if config is None:
        config = _make_config()
    checkpoint_store = TorchSaveCheckpointStore(tmp_dir)
    scheduled_weights = ScheduledWeights(1)
    controller = CurriculumController(
        config, checkpoint_store, scheduled_weights,
        run_controller=run_controller,
        forced_disposition=forced_disposition,
        recover_retries=recover_retries,
        initial_stage=initial_stage,
    )
    return controller, checkpoint_store


# ---------------------------------------------------------------------------
# Construction / T-40-09 guard.
# ---------------------------------------------------------------------------

class CurriculumControllerConstructionTests(unittest.TestCase):
    def setUp(self):
        self.CurriculumController = _require("CurriculumController")
        self.ForcedDispositionOnLiveRun = _require("ForcedDispositionOnLiveRun")
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def _dummy_run_controller(self):
        return mock.Mock(name="live_run_controller")

    def test_forced_disposition_defaults_to_absent(self):
        sig = inspect.signature(self.CurriculumController.__init__)
        self.assertIn("forced_disposition", sig.parameters)
        self.assertIsNone(sig.parameters["forced_disposition"].default)

    def test_forced_disposition_alongside_live_run_controller_raises_at_construction(self):
        checkpoint_store = TorchSaveCheckpointStore(self._tmpdir.name)
        scheduled_weights = ScheduledWeights(1)
        with self.assertRaises(self.ForcedDispositionOnLiveRun):
            self.CurriculumController(
                _make_config(), checkpoint_store, scheduled_weights,
                run_controller=self._dummy_run_controller(),
                forced_disposition=lambda k: StageDisposition.ADVANCE,
            )

    def test_exactly_one_guard_mechanism_no_alternative_assert_unset(self):
        """T-40-09: the raise is the ONLY guard -- no parallel 'assert unset'
        code path exists anywhere in the class body."""
        init_source = inspect.getsource(self.CurriculumController.__init__)
        self.assertIn("ForcedDispositionOnLiveRun", init_source)
        full_source = inspect.getsource(self.CurriculumController)
        assert_lines = [
            ln for ln in full_source.splitlines() if ln.strip().startswith("assert ")
        ]
        self.assertEqual(
            assert_lines, [],
            f"found an alternative assert-based guard: {assert_lines!r}",
        )

    def test_forced_disposition_only_construction_does_not_raise(self):
        controller, _store = _minimal_controller(
            self._tmpdir.name, forced_disposition=lambda k: StageDisposition.HALT,
        )
        self.assertEqual(controller.stage, 0)
        self.assertFalse(controller.halted)

    def test_stage_factory_defaults_to_none(self):
        """GAP-40-04 / PLAT-01: stage_factory is opt-in; default preserves single-stage."""
        sig = inspect.signature(self.CurriculumController.__init__)
        self.assertIn("stage_factory", sig.parameters)
        self.assertIsNone(sig.parameters["stage_factory"].default)

    def test_stage_factory_alongside_forced_disposition_raises_at_construction(self):
        """T-40-09: stage_factory is a live-run construct; same single guard."""
        checkpoint_store = TorchSaveCheckpointStore(self._tmpdir.name)
        scheduled_weights = ScheduledWeights(1)

        def _factory(_k):
            raise AssertionError("factory must not be called at construction")

        with self.assertRaises(self.ForcedDispositionOnLiveRun):
            self.CurriculumController(
                _make_config(), checkpoint_store, scheduled_weights,
                stage_factory=_factory,
                forced_disposition=lambda k: StageDisposition.ADVANCE,
            )


# ---------------------------------------------------------------------------
# Forced-disposition dispatch (ADVANCE / HALT / RECOVER).
# ---------------------------------------------------------------------------

class ForcedDispositionDispatchTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_forced_advance_yields_delta_stage_plus_one_and_saves_anchors(self):
        controller, store = _minimal_controller(
            self._tmpdir.name, forced_disposition=lambda k: StageDisposition.ADVANCE,
        )
        save_spy = mock.Mock(wraps=store.save)
        with mock.patch.object(store, "save", save_spy):
            disposition = controller.step()
        self.assertEqual(disposition, StageDisposition.ADVANCE)
        self.assertEqual(controller.stage, 1)
        tags = [call.args[0]["tag"] for call in save_spy.call_args_list]
        self.assertEqual(tags, ["stage-0-final", "stage-1-init"])

    def test_forced_halt_yields_delta_stage_zero(self):
        controller, _store = _minimal_controller(
            self._tmpdir.name, forced_disposition=lambda k: StageDisposition.HALT,
        )
        disposition = controller.step()
        self.assertEqual(disposition, StageDisposition.HALT)
        self.assertEqual(controller.stage, 0)
        self.assertTrue(controller.halted)

    def test_forced_recover_at_retries_zero_rolls_back_and_halts_with_no_retrain(self):
        controller, store = _minimal_controller(
            self._tmpdir.name, forced_disposition=lambda k: StageDisposition.RECOVER,
            recover_retries=0,
        )
        # Seed a well-formed checkpoint so rollback() SUCCEEDS -- the empty
        # store / cold-start case is a dedicated test below.
        store.save({"tag": "seed", "stage": 0})
        rollback_spy = mock.Mock(wraps=store.rollback)
        with mock.patch.object(store, "rollback", rollback_spy):
            disposition = controller.step()
        self.assertEqual(rollback_spy.call_count, 1)
        self.assertEqual(disposition, StageDisposition.HALT)
        self.assertEqual(controller.stage, 0)
        self.assertTrue(controller.halted)


# ---------------------------------------------------------------------------
# Cold-start RECOVER against a genuinely empty CheckpointStore (cycle-2 H3).
# ---------------------------------------------------------------------------

class ColdStartRecoverTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_recover_against_empty_checkpoint_store_does_not_crash(self):
        controller, store = _minimal_controller(
            self._tmpdir.name, forced_disposition=lambda k: StageDisposition.RECOVER,
            recover_retries=0,
        )
        self.assertEqual(store._ids, [])  # genuinely empty -- no prior save

        # Suppress the run-start anchor so the store stays genuinely empty
        # (the anchor itself is a SEPARATE test below); the call is NOT
        # wrapped in assertRaises -- run() must return normally.
        with mock.patch.object(controller, "_save_run_start_anchor"):
            disposition = controller.run()

        self.assertEqual(disposition, StageDisposition.HALT)
        self.assertEqual(controller.stage, 0)
        self.assertTrue(controller.halted)


# ---------------------------------------------------------------------------
# CR-01 / WR-05 — RECOVER restores rolled-back checkpoint state (behavioral).
# ---------------------------------------------------------------------------

class RecoverRestoreBehavioralTests(unittest.TestCase):
    """Behavioral RECOVER-restore coverage (closes CR-01; replaces WR-05 grep).

    Asserts on live model parameter tensors after a real RunController
    RECOVER path — not on rollback spy call counts or source-text greps.
    """

    def setUp(self):
        self.RunController = _require("RunController")
        self.CurriculumController = _require("CurriculumController")
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def _build_live_curriculum(self, *, recover_retries: int):
        runtime = resolve_runtime("float64", "cpu")
        model = make_stub_model(dtype=runtime.dtype, device=runtime.torch_device)
        train_source, validation_source = make_stub_split_sources(
            n_train=300, n_validation=300,
        )
        config = _make_config(max_epochs=3, n_adam=3)
        scheduled_weights = ScheduledWeights(1, lambda_e_max=0.0, lambda_l_max=0.0)
        grad_clipper = GradClipper()
        collocation_sampler = CollocationSampler(2, np.random.default_rng(0))
        stage_exit_machine = StageExitMachine(config)
        checkpoint_store = TorchSaveCheckpointStore(self._tmpdir.name)
        run_controller = self.RunController(
            model, train_source, validation_source, config,
            scheduled_weights, grad_clipper, collocation_sampler,
            stage_exit_machine, checkpoint_store, runtime,
            rng=np.random.default_rng(1),
        )
        controller = self.CurriculumController(
            config, checkpoint_store, scheduled_weights,
            run_controller=run_controller,
            recover_retries=recover_retries,
        )
        return controller, run_controller, model

    @staticmethod
    def _nan_compose(run_controller):
        dtype, device = run_controller._dtype, run_controller._device
        zero = torch.zeros((), dtype=dtype, device=device)

        def fake_compose(batch, anchor_ctx, weights):
            return LossTerms(
                data=zero, ic=zero,
                phys=torch.tensor(1.0, dtype=dtype, device=device),
                energy=zero, angmom=zero,
                total=torch.tensor(float("nan"), dtype=dtype, device=device),
            )

        return fake_compose

    def test_recover_with_retries_restores_model_params_from_checkpoint(self):
        controller, run_controller, model = self._build_live_curriculum(
            recover_retries=1,
        )
        # (1) Snapshot known-good parameters (clone — state_dict views alias).
        reference = [p.detach().clone() for p in model.parameters()]
        # (2) Save anchor through the controller's own payload path so the
        # stored payload carries run_controller.
        controller._save_run_start_anchor()
        # (3) Mutate live parameters so a no-op restore is distinguishable.
        with torch.no_grad():
            for p in model.parameters():
                p.add_(1.0)
        for p, ref in zip(model.parameters(), reference):
            self.assertFalse(
                torch.allclose(p, ref),
                "mutation step must make live params differ from the seed",
            )
        # (4) Drive a REAL RunController to RECOVER via the sanctioned seam.
        with mock.patch.object(
            run_controller, "_compose_loss_terms",
            side_effect=self._nan_compose(run_controller),
        ):
            disposition = controller.step()
        # (5) Retry authorized at recover_retries=1 → RECOVER, and params
        # restored from the rolled-back checkpoint (CR-01).
        self.assertEqual(disposition, StageDisposition.RECOVER)
        for p, ref in zip(model.parameters(), reference):
            self.assertTrue(
                torch.allclose(p, ref),
                "RECOVER must restore model parameters from the rolled-back "
                "checkpoint (CR-01)",
            )

    def test_recover_at_retries_zero_restores_then_halts_with_no_retrain(self):
        controller, run_controller, model = self._build_live_curriculum(
            recover_retries=0,
        )
        reference = [p.detach().clone() for p in model.parameters()]
        controller._save_run_start_anchor()
        with torch.no_grad():
            for p in model.parameters():
                p.add_(1.0)
        for p, ref in zip(model.parameters(), reference):
            self.assertFalse(torch.allclose(p, ref))

        with mock.patch.object(
            run_controller, "_compose_loss_terms",
            side_effect=self._nan_compose(run_controller),
        ):
            disposition = controller.step()

        self.assertEqual(disposition, StageDisposition.HALT)
        self.assertEqual(controller.stage, 0)
        self.assertTrue(controller.halted)
        for p, ref in zip(model.parameters(), reference):
            self.assertTrue(
                torch.allclose(p, ref),
                "recover_retries=0 still restores, then HALTs with no retrain",
            )

    def test_live_run_controller_recover_against_empty_store_does_not_crash(self):
        """Empty-store backstop with a LIVE RunController (restore path).

        Forced-disposition coverage already exists in ColdStartRecoverTests;
        this case reaches the restore code inside the guarded region that a
        forced-disposition controller never exercises.
        """
        controller, run_controller, _model = self._build_live_curriculum(
            recover_retries=0,
        )
        with mock.patch.object(controller, "_save_run_start_anchor"), \
             mock.patch.object(
                 run_controller, "_compose_loss_terms",
                 side_effect=self._nan_compose(run_controller),
             ):
            disposition = controller.run()

        self.assertEqual(disposition, StageDisposition.HALT)
        self.assertEqual(controller.stage, 0)
        self.assertTrue(controller.halted)


# ---------------------------------------------------------------------------
# sL-BFGS preflight gate (TRAIN-07 wiring).
# ---------------------------------------------------------------------------

class PreflightGateTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_advancing_into_stage_three_raises_before_run_stage(self):
        controller, _store = _minimal_controller(
            self._tmpdir.name, forced_disposition=lambda k: StageDisposition.ADVANCE,
        )
        with mock.patch.object(controller, "_save_run_start_anchor"), \
             mock.patch.object(controller, "_log_run_start"):
            with self.assertRaises(StochasticLBFGSNotImplemented) as ctx:
                controller.run()
        self.assertEqual(ctx.exception.stage, 3)
        self.assertEqual(controller.stage, 3)  # 0->1->2->3 via three ADVANCEs, then refused


# ---------------------------------------------------------------------------
# CTX-38/45 run-start logging + run-start anchor ordering.
# ---------------------------------------------------------------------------

class RunStartLoggingAndAnchorTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_run_start_logs_provisional_threshold_set_with_provenance(self):
        config = _make_config()
        controller, _store = _minimal_controller(
            self._tmpdir.name, forced_disposition=lambda k: StageDisposition.HALT,
            config=config,
        )
        with self.assertLogs("pinn.training", level="INFO") as cm:
            controller.run()
        joined = "\n".join(cm.output)
        self.assertIn("provisional", joined.lower())
        for field in config.provisional_fields():
            self.assertIn(field["name"], joined)
            self.assertIn(field["provenance"], joined)

    def test_run_start_anchor_saved_before_first_stage(self):
        controller, store = _minimal_controller(
            self._tmpdir.name,
            forced_disposition=(
                lambda k: StageDisposition.ADVANCE if k == 0 else StageDisposition.HALT
            ),
        )
        save_spy = mock.Mock(wraps=store.save)
        with mock.patch.object(store, "save", save_spy):
            controller.run()
        self.assertGreaterEqual(save_spy.call_count, 1)
        first_payload = save_spy.call_args_list[0].args[0]
        self.assertEqual(first_payload["tag"], "stage-0-init")


# ---------------------------------------------------------------------------
# Composed, gate-earned ADVANCE through a REAL (non-forced) RunController
# (cycle-2 M4 -- closes the "ADVANCE is only ever force-injected" gap).
# ---------------------------------------------------------------------------

class ComposedGateEarnedAdvanceTests(unittest.TestCase):
    def setUp(self):
        self.RunController = _require("RunController")
        self.CurriculumController = _require("CurriculumController")
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_real_run_stage_produces_advance_with_permissive_test_local_thresholds(self):
        """TEST-LOCAL permissive thresholds exercise the ADVANCE gate's FORM
        through the real path (RunController.run_stage -> StageExitMachine).

        ``eps_plateau``/``eps_phys``/``eps_energy`` are set to 1e15 and
        ``patience=1`` so the real (untrained, stub-model) Stage-0 forward
        pass genuinely satisfies all four ADVANCE criteria within a single
        L-BFGS epoch -- an UNTRAINED SIREN network (omega_0=30) produces a
        physics-residual magnitude in the 1e9-1e10 range on random init, so
        the permissive threshold must clear that mechanism-noise floor, not
        a real convergence bar. These are MECHANISM values chosen to make
        the gate's FORM observable on cheap fixtures -- they are NOT
        calibrated pass levels, assert nothing about real-data convergence,
        and do not touch any config default. Whether Stage 0 actually earns
        an ADVANCE on real data under calibrated thresholds remains Phase 43
        (ACC-05).
        """
        runtime = resolve_runtime("float64", "cpu")
        model = make_stub_model(dtype=runtime.dtype, device=runtime.torch_device)
        train_source, validation_source = make_stub_split_sources(n_train=300, n_validation=300)
        config = _make_config(
            max_epochs=2, n_adam=1, validation_every=2,
            beta=0.5, patience=1,
            eps_plateau=1e15, eps_phys=1e15, eps_energy=1e15,
            lbfgs_chunk_size=8, lbfgs_max_iter=2,
        )
        scheduled_weights = ScheduledWeights(1, lambda_e_max=0.0, lambda_l_max=0.0)
        grad_clipper = GradClipper()
        collocation_sampler = CollocationSampler(2, np.random.default_rng(0))
        stage_exit_machine = StageExitMachine(config)
        checkpoint_store = TorchSaveCheckpointStore(self._tmpdir.name)
        run_controller = self.RunController(
            model, train_source, validation_source, config,
            scheduled_weights, grad_clipper, collocation_sampler,
            stage_exit_machine, checkpoint_store, runtime,
            rng=np.random.default_rng(1),
        )
        controller = self.CurriculumController(
            config, checkpoint_store, scheduled_weights,
            run_controller=run_controller,
        )

        disposition = controller.step()

        self.assertEqual(disposition, StageDisposition.ADVANCE)
        self.assertEqual(controller.stage, 1)


# ---------------------------------------------------------------------------
# GAP-40-04 / CR-03 — stage_factory seam (Option C): per-stage RunController
# swap on ADVANCE, model continuity, anchor provenance, composed RECOVER.
# ---------------------------------------------------------------------------

class StageFactorySeamTests(unittest.TestCase):
    """Task 1 ACs for the GAP-40-04 stage_factory Option C seam.

    Uses a live RunController whose ``run_stage`` is mocked to return ADVANCE
    (or RECOVER) so the tests exercise the ADVANCE-branch swap / rebind /
    anchor ordering without paying for a full earned-gate training pass. The
    live-objective AC (Task 2) is the physics proof on a non-mocked path.
    """

    STAGE0_LAMBDA_PHYS = 1.0
    STAGE1_LAMBDA_PHYS = 7.0

    def setUp(self):
        self.RunController = _require("RunController")
        self.CurriculumController = _require("CurriculumController")
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.runtime = resolve_runtime("float64", "cpu")
        self.model = make_stub_model(
            dtype=self.runtime.dtype, device=self.runtime.torch_device,
        )
        # Stage-1 records required so a real stage-1 run_stage can build a
        # batch (composed RECOVER path). Population sized to clear
        # StageZeroUnderpopulated / select_stage_records floors (240 replay).
        self.train_source = make_stub_source(
            n_stage0=300, n_stage1=300, id_offset=0,
        )
        self.validation_source = make_stub_source(
            n_stage0=300, n_stage1=300, id_offset=50_000,
        )
        self.config = _make_config(max_epochs=2, n_adam=1)
        self.checkpoint_store = TorchSaveCheckpointStore(self._tmpdir.name)

    def _require_model_mismatch(self):
        return _require("StageFactoryModelMismatch")

    def _build_run_controller(self, *, model, lambda_phys_max, n_adam=1):
        scheduled = ScheduledWeights(
            n_adam,
            lambda_phys_max=lambda_phys_max,
            lambda_e_max=0.0,
            lambda_l_max=0.0,
        )
        return self.RunController(
            model, self.train_source, self.validation_source, self.config,
            scheduled, GradClipper(),
            CollocationSampler(2, np.random.default_rng(0)),
            StageExitMachine(self.config), self.checkpoint_store, self.runtime,
            rng=np.random.default_rng(1),
        )

    def _build_curriculum(self, *, stage0_rc, stage_factory, recover_retries=0):
        # Prefer the public read-only accessor once present; fall back to the
        # private field so RED against pre-seam code fails on stage_factory
        # (TypeError) rather than on a missing property.
        try:
            stage0_weights = stage0_rc.scheduled_weights
        except AttributeError:
            stage0_weights = stage0_rc._scheduled_weights
        return self.CurriculumController(
            self.config, self.checkpoint_store,
            stage0_weights,
            run_controller=stage0_rc,
            stage_factory=stage_factory,
            recover_retries=recover_retries,
        )

    def test_model_continuity_preserved_across_factory_swap(self):
        stage0 = self._build_run_controller(
            model=self.model, lambda_phys_max=self.STAGE0_LAMBDA_PHYS,
        )
        stage1 = self._build_run_controller(
            model=self.model, lambda_phys_max=self.STAGE1_LAMBDA_PHYS,
        )
        factory_calls = []

        def factory(k):
            factory_calls.append(k)
            self.assertEqual(k, 1)
            return stage1

        controller = self._build_curriculum(
            stage0_rc=stage0, stage_factory=factory,
        )
        pre_swap_params = [p.detach().clone() for p in self.model.parameters()]
        with mock.patch.object(
            stage0, "run_stage", return_value=StageDisposition.ADVANCE,
        ):
            disposition = controller.step()

        self.assertEqual(disposition, StageDisposition.ADVANCE)
        self.assertEqual(controller.stage, 1)
        self.assertEqual(factory_calls, [1])
        self.assertIs(controller._run_controller, stage1)
        self.assertIs(controller._run_controller.model, self.model)
        self.assertIs(
            controller._scheduled_weights,
            controller._run_controller.scheduled_weights,
        )
        self.assertIs(
            controller._scheduled_weights,
            stage1.scheduled_weights,
        )
        self.assertEqual(
            controller._scheduled_weights.state_dict()["lambda_phys_max"],
            self.STAGE1_LAMBDA_PHYS,
        )
        for p, ref in zip(self.model.parameters(), pre_swap_params):
            self.assertTrue(
                torch.allclose(p, ref),
                "factory swap itself must not modify model parameter tensors",
            )

    def test_foreign_model_from_factory_raises_and_does_not_partial_swap(self):
        StageFactoryModelMismatch = self._require_model_mismatch()
        stage0 = self._build_run_controller(
            model=self.model, lambda_phys_max=self.STAGE0_LAMBDA_PHYS,
        )
        foreign_model = make_stub_model(
            dtype=self.runtime.dtype, device=self.runtime.torch_device,
        )
        foreign_stage1 = self._build_run_controller(
            model=foreign_model, lambda_phys_max=self.STAGE1_LAMBDA_PHYS,
        )
        try:
            stage0_weights = stage0.scheduled_weights
        except AttributeError:
            stage0_weights = stage0._scheduled_weights

        def factory(_k):
            return foreign_stage1

        controller = self._build_curriculum(
            stage0_rc=stage0, stage_factory=factory,
        )
        with mock.patch.object(
            stage0, "run_stage", return_value=StageDisposition.ADVANCE,
        ):
            with self.assertRaises(StageFactoryModelMismatch):
                controller.step()

        # No partial swap: live controller and schedule remain stage 0's.
        self.assertIs(controller._run_controller, stage0)
        self.assertIs(controller._scheduled_weights, stage0_weights)
        # Rebind nothing before the model-continuity check passes. The ruled
        # sequence sets stage = k+1 before the factory call, so stage may
        # already be 1 on raise; the load-bearing invariant is no rebind.
        self.assertIs(controller._run_controller.model, self.model)

    def test_anchor_provenance_final_from_old_init_from_new(self):
        stage0 = self._build_run_controller(
            model=self.model, lambda_phys_max=self.STAGE0_LAMBDA_PHYS,
        )
        stage1 = self._build_run_controller(
            model=self.model, lambda_phys_max=self.STAGE1_LAMBDA_PHYS,
        )

        def factory(_k):
            return stage1

        controller = self._build_curriculum(
            stage0_rc=stage0, stage_factory=factory,
        )
        save_spy = mock.Mock(wraps=self.checkpoint_store.save)
        with mock.patch.object(self.checkpoint_store, "save", save_spy), \
             mock.patch.object(
                 stage0, "run_stage", return_value=StageDisposition.ADVANCE,
             ):
            disposition = controller.step()

        self.assertEqual(disposition, StageDisposition.ADVANCE)
        tags = [call.args[0]["tag"] for call in save_spy.call_args_list]
        self.assertEqual(tags, ["stage-0-final", "stage-1-init"])
        final_payload = save_spy.call_args_list[0].args[0]
        init_payload = save_spy.call_args_list[1].args[0]
        final_max = final_payload["run_controller"]["scheduled_weights"][
            "lambda_phys_max"
        ]
        init_max = init_payload["run_controller"]["scheduled_weights"][
            "lambda_phys_max"
        ]
        self.assertEqual(final_max, self.STAGE0_LAMBDA_PHYS)
        self.assertEqual(init_max, self.STAGE1_LAMBDA_PHYS)

    def test_composed_swap_anchor_recover_keeps_stage1_lambda_max(self):
        """W4: swap → stage-1-init → RECOVER restore leaves stage-1 caps live.

        Proves the joint path, not two halves: after a factory-swapped ADVANCE
        the stage-1-init anchor must carry stage 1's lambda^max so a RECOVER
        restore cannot re-pin the objective to stage 0 (T-40-13 / CR-03).
        """
        stage0 = self._build_run_controller(
            model=self.model, lambda_phys_max=self.STAGE0_LAMBDA_PHYS,
        )
        stage1 = self._build_run_controller(
            model=self.model, lambda_phys_max=self.STAGE1_LAMBDA_PHYS,
        )

        def factory(_k):
            return stage1

        controller = self._build_curriculum(
            stage0_rc=stage0, stage_factory=factory, recover_retries=1,
        )
        with mock.patch.object(
            stage0, "run_stage", return_value=StageDisposition.ADVANCE,
        ):
            self.assertEqual(controller.step(), StageDisposition.ADVANCE)
        self.assertEqual(controller.stage, 1)
        self.assertIs(controller._run_controller, stage1)

        # Snapshot stage-1-init anchored params, then mutate live weights.
        reference = [p.detach().clone() for p in self.model.parameters()]
        with torch.no_grad():
            for p in self.model.parameters():
                p.add_(1.0)
        for p, ref in zip(self.model.parameters(), reference):
            self.assertFalse(torch.allclose(p, ref))

        dtype, device = stage1._dtype, stage1._device
        zero = torch.zeros((), dtype=dtype, device=device)

        def nan_compose(batch, anchor_ctx, weights):
            return LossTerms(
                data=zero, ic=zero,
                phys=torch.tensor(1.0, dtype=dtype, device=device),
                energy=zero, angmom=zero,
                total=torch.tensor(float("nan"), dtype=dtype, device=device),
            )

        with mock.patch.object(
            stage1, "_compose_loss_terms", side_effect=nan_compose,
        ):
            disposition = controller.step()

        self.assertEqual(disposition, StageDisposition.RECOVER)
        for p, ref in zip(self.model.parameters(), reference):
            self.assertTrue(
                torch.allclose(p, ref),
                "RECOVER must restore model params (proves 40-07 restore ran)",
            )
        live_max = controller._run_controller.scheduled_weights.state_dict()[
            "lambda_phys_max"
        ]
        self.assertEqual(
            live_max, self.STAGE1_LAMBDA_PHYS,
            "restore must leave stage-1 lambda^max live (swap precedes init save)",
        )
        self.assertNotEqual(live_max, self.STAGE0_LAMBDA_PHYS)


# ---------------------------------------------------------------------------
# GAP-40-04 live-objective AC (TRAIN-01) — the physics proof that CR-03 is
# closed for real: weights reaching _compose_loss_terms after ADVANCE carry
# stage 1's lambda^max, not stage 0's. Observed on the real :479→:482 path
# of a live non-forced RunController. A factory call-count is NOT the proof.
# ---------------------------------------------------------------------------

class LiveObjectiveStageFactoryTests(unittest.TestCase):
    """Replacement TRAIN-01 AC from GAP-40-04 Resolution note.

    MECHANISM values only (permissive thresholds, distinct lambda_phys_max,
    small n_adam so I_warm==0 and ramp saturates at 1.0). Not calibrated pass
    levels; assert nothing about real-data convergence; touch no config
    default. Per-stage values arrive THROUGH the factory seam exactly as an
    owner would supply them (SCOPE-19). Whether stage 1 earns ADVANCE on real
    data under calibrated thresholds remains Phase 43 (ACC-05).
    """

    STAGE0_LAMBDA_PHYS = 1.0
    STAGE1_LAMBDA_PHYS = 7.0
    TOL = 1e-12

    def setUp(self):
        self.RunController = _require("RunController")
        self.CurriculumController = _require("CurriculumController")
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_stage1_compose_receives_stage1_lambda_phys_max(self):
        runtime = resolve_runtime("float64", "cpu")
        model = make_stub_model(dtype=runtime.dtype, device=runtime.torch_device)
        # Stage-1 records required for stage-1 run_stage batch construction.
        # Disjoint id_offset mirrors make_stub_split_sources key separation.
        train_source = make_stub_source(n_stage0=300, n_stage1=300, id_offset=0)
        validation_source = make_stub_source(
            n_stage0=300, n_stage1=300, id_offset=50_000,
        )
        # n_adam=1 → I_warm = min(2000, int(0.1*1)) = 0 → ramp == 1.0, so
        # lambda_phys == lambda_phys_max exactly (clean equality to tol).
        config = _make_config(
            max_epochs=2, n_adam=1, validation_every=2,
            beta=0.5, patience=1,
            eps_plateau=1e15, eps_phys=1e15, eps_energy=1e15,
            lbfgs_chunk_size=8, lbfgs_max_iter=2,
        )
        stage0_weights = ScheduledWeights(
            1,
            lambda_phys_max=self.STAGE0_LAMBDA_PHYS,
            lambda_e_max=0.0,
            lambda_l_max=0.0,
        )
        checkpoint_store = TorchSaveCheckpointStore(self._tmpdir.name)
        stage0_rc = self.RunController(
            model, train_source, validation_source, config,
            stage0_weights, GradClipper(),
            CollocationSampler(2, np.random.default_rng(0)),
            StageExitMachine(config), checkpoint_store, runtime,
            rng=np.random.default_rng(1),
        )

        def stage_factory(k):
            # Permissive thresholds can earn ADVANCE at stage 1 too; factory
            # must accept k>=1. Discriminator is lambda_phys_max for k==1
            # (stage 0 uses STAGE0_LAMBDA_PHYS via the seed controller).
            lambda_phys = (
                self.STAGE1_LAMBDA_PHYS if k == 1 else self.STAGE1_LAMBDA_PHYS
            )
            stage_k_weights = ScheduledWeights(
                1,
                lambda_phys_max=lambda_phys,
                lambda_e_max=0.0,
                lambda_l_max=0.0,
            )
            # SAME model instance (model-continuity invariant).
            return self.RunController(
                model, train_source, validation_source, config,
                stage_k_weights, GradClipper(),
                CollocationSampler(2, np.random.default_rng(2 + k)),
                StageExitMachine(config), checkpoint_store, runtime,
                rng=np.random.default_rng(3 + k),
            )

        controller = self.CurriculumController(
            config, checkpoint_store, stage0_weights,
            run_controller=stage0_rc,
            stage_factory=stage_factory,
        )

        # (1) Earn ADVANCE at stage 0 through the real gate path.
        disposition = controller.step()
        self.assertEqual(disposition, StageDisposition.ADVANCE)
        self.assertEqual(controller.stage, 1)
        self.assertIs(controller._run_controller.model, model)

        # (2) Capture weights reaching _compose_loss_terms on the NEW live
        # controller; delegate to the real implementation so run_stage stays real.
        captured = []
        real_compose = controller._run_controller._compose_loss_terms

        def recording_compose(batch, anchor_ctx, weights):
            captured.append(weights)
            return real_compose(batch, anchor_ctx, weights)

        with mock.patch.object(
            controller._run_controller, "_compose_loss_terms",
            side_effect=recording_compose,
        ):
            # (3) Train stage 1 for real (preflight accepts stages {0,1,2}).
            controller.step()

        self.assertGreater(
            len(captured), 0,
            "stage-1 composition path must execute (non-vacuous capture)",
        )
        # (4) Live-objective AC: composed lambda_phys is stage 1's, not stage 0's.
        observed = [float(w.lambda_phys) for w in captured]
        for lp in observed:
            self.assertLessEqual(
                abs(lp - self.STAGE1_LAMBDA_PHYS), self.TOL,
                f"composed lambda_phys={lp} must equal stage-1 max "
                f"{self.STAGE1_LAMBDA_PHYS}",
            )
            self.assertGreater(
                abs(lp - self.STAGE0_LAMBDA_PHYS), self.TOL,
                f"composed lambda_phys={lp} must NOT equal stage-0 max "
                f"{self.STAGE0_LAMBDA_PHYS}",
            )
        # Cheap companion pin on the schedule object itself.
        pin = controller._run_controller.scheduled_weights.current(0).lambda_phys
        self.assertLessEqual(abs(float(pin) - self.STAGE1_LAMBDA_PHYS), self.TOL)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
