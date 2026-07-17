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

    def test_recover_branch_catches_empty_checkpoint_store(self):
        CurriculumController = _require("CurriculumController")
        source = inspect.getsource(CurriculumController)
        self.assertIn("except EmptyCheckpointStore", source)


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


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
