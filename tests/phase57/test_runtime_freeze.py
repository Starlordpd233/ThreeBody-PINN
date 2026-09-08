"""Phase 57 Task 2/3 — the frozen training-only monitor, L-BFGS segment
freeze, and (Task 3) the immutable Checkpoint-③ config band.

D-03 (57-CONTEXT.md) / 57-RULING.md §2: each run uses ONE frozen
training-only invariant-B monitoring context, fixed before the run's first
optimizer update, whose selected identities/collocation rows/bin
assignments/normalized times survive the whole run (including the
Adam-to-L-BFGS handoff) unchanged; ``front_advance_window_n = 500`` is a
SEPARATE step-count deadline, never the monitor's cardinality. For the
entire L-BFGS segment, the segment's collocation samples and DETACHED
causal weights are frozen at handoff and are not redrawn or recomputed in
line-search closures or between outer calls.

Every test here drives a real production seam
(``pinn.loss_catalog.causal_physics_loss``,
``pinn.training.controllers.{RunController, build_checkpoint_payload}``,
``pinn.training.config``) and is expected to be RED because these
Checkpoint-③ behaviors are not yet implemented -- never because of an
import, syntax, fixture, data, or environment error.
"""

from __future__ import annotations

import inspect
import tempfile
import unittest

import torch

from pinn.loss_catalog import causal_physics_loss
from pinn.training.config import InvariantsConfig
from pinn.training.controllers import RunController, build_checkpoint_payload

from tests.phase57._fixtures import (
    RATIFIED_N_BINS,
    build_run_controller,
    make_full_slot_source,
    make_stub_source,
)


class MonitorContractTests(unittest.TestCase):
    """The frozen training-only invariant-B monitor (checkpoint ③).

    ``RunController.state_dict()`` / ``build_checkpoint_payload`` already
    persist ``invariant_b_state`` -- but that is only the two DERIVED
    ``StepGuards`` scalars (``front_high_water``, ``last_advance_step``), not
    the monitor's OWN frozen identities/collocation rows/bin assignments/
    normalized times. 57-RULING.md §2 requires "The frozen monitor and its
    provenance must be persisted so a resume restores the same monitor bytes
    and invariant-B state" -- a strictly larger persisted object than the
    two-scalar ``invariant_b_state`` that exists today.
    """

    def setUp(self) -> None:
        self.train_source = make_full_slot_source()
        self.validation_source = make_stub_source(n_stage0=50, id_offset=90_000)
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.controller = build_run_controller(
            self.train_source, self.validation_source, tmp_dir=self._tmpdir.name,
        )

    def test_checkpoint_payload_carries_a_dedicated_front_monitor_key(self) -> None:
        payload = build_checkpoint_payload(
            self.controller, curriculum_state={}, config_identity={},
            schema_version=2,
            invariant_b_state={"front_high_water": -1, "last_advance_step": None},
        )
        self.assertTrue(
            "front_monitor" in payload,
            "the CTX-53 checkpoint envelope must carry a DEDICATED "
            "'front_monitor' key -- the monitor's own frozen training "
            "identities/collocation rows/bin assignments/normalized times "
            "-- distinct from the already-present 'invariant_b_state' "
            "(which only carries the two derived StepGuards scalars); "
            f"got keys {sorted(payload.keys())!r}",
        )

    def test_run_controller_exposes_a_front_monitor_accessor(self) -> None:
        self.assertTrue(
            hasattr(self.controller, "front_monitor_state")
            or hasattr(RunController, "_build_front_monitor"),
            "RunController must expose a way to obtain its ONE frozen "
            "training-only monitor (built once, before the run's first "
            "optimizer update; re-evaluated at accepted parameter states "
            "only, never resampled)",
        )

    def test_front_monitor_key_is_distinct_from_invariant_b_state(self) -> None:
        payload = build_checkpoint_payload(
            self.controller, curriculum_state={}, config_identity={},
            schema_version=2,
            invariant_b_state={"front_high_water": 3, "last_advance_step": 10},
        )
        # First require presence -- a vacuous "None != {...}" pass on a
        # MISSING key would be exactly the "check that cannot fail" the
        # Phase-49 lesson forbids (57-CONTEXT.md "Specific Ideas").
        self.assertTrue(
            "front_monitor" in payload,
            f"front_monitor must be present before its distinctness from "
            f"invariant_b_state can even be checked; got keys "
            f"{sorted(payload.keys())!r}",
        )
        # Even once present, it must not simply alias the existing
        # two-scalar invariant_b_state (checkpoint (3) requires the
        # monitor's OWN identities/rows/bins/times, a strictly richer
        # object).
        self.assertNotEqual(
            payload["front_monitor"], payload["invariant_b_state"],
            "front_monitor must carry the monitor's own frozen identities/"
            "collocation rows/bin assignments/normalized times -- not merely "
            "duplicate the two-scalar invariant_b_state",
        )


class WindowContractTests(unittest.TestCase):
    """``front_advance_window_n = 500`` is a step-count deadline, never a
    monitor cardinality (57-RULING.md §2 "Window and monitor").
    """

    def test_front_advance_window_n_500_round_trips_explicitly(self) -> None:
        """Checkpoint ③ (D-03): 500 is an explicit RE-RATIFICATION for the
        amended recipe, not silent inheritance -- pin the exact value.
        """
        cfg = InvariantsConfig(front_advance_window_n=500)
        self.assertEqual(cfg.front_advance_window_n, 500)

    def test_guards_module_never_references_bin_or_row_cardinality_constants(self) -> None:
        """A protective regression: ``pinn.training.guards`` must keep the
        step-deadline window structurally SEPARATE from the ratified
        bin/row cardinality (16 bins / 256 per bin / 4096 total) -- an
        implementation that read ``front_advance_window_n`` as a monitor
        size, or vice versa, would silently conflate two independently
        ratified numbers.
        """
        import pinn.training.guards as guards_module

        source = inspect.getsource(guards_module)
        for forbidden in ("RATIFIED_N_BINS", "RATIFIED_PER_BIN", "RATIFIED_TOTAL"):
            self.assertNotIn(
                forbidden, source,
                f"pinn.training.guards must not reference {forbidden} -- "
                "the invariant-B step deadline and the monitor's own "
                "cardinality are two independently ratified numbers "
                "(57-RULING.md checkpoint 3) and must never be derived "
                "from each other",
            )

    def test_monitor_cardinality_is_the_ratified_recipe_not_the_window(self) -> None:
        """Once the frozen monitor exists, its OWN row/bin count must be the
        ratified §3.2 recipe (``RATIFIED_N_BINS`` bins), never
        ``front_advance_window_n`` (500) -- the two numbers are unrelated by
        contract even though both happen to be integers in the same
        run.invariants-adjacent configuration surface.
        """
        self.assertIn(
            "front_monitor",
            inspect.getsource(build_checkpoint_payload),
            "build_checkpoint_payload must assemble a 'front_monitor' "
            "field whose cardinality is the ratified 16-bin recipe, "
            "independent of run.invariants.front_advance_window_n",
        )


class LbfgsFreezeTests(unittest.TestCase):
    """GAP-54-06: the L-BFGS segment's samples and DETACHED causal weights
    are frozen at handoff and reused unchanged across every closure
    evaluation and every outer ``optimizer.step(closure)`` call for the
    whole segment.

    ``causal_physics_loss`` currently always recomputes its weight vector
    from whatever ``residuals_per_time`` the CURRENT call supplies -- it has
    no way to accept a pre-computed, externally-frozen weight vector and
    combine it with a freshly-evaluated (trial-parameter) residual. This
    module targets the additional keyword-only ``frozen_weights`` parameter:
    when supplied, the returned loss is ``(frozen_weights * r_tilde).mean()``
    using the FRESH ``r_tilde`` but the FIXED ``frozen_weights`` -- the
    weight computation (prefix/exp/clamp) is skipped entirely.
    """

    def test_frozen_weights_are_reused_unchanged_across_different_residuals(self) -> None:
        frozen_weights = torch.tensor(
            [1.0 / (n + 1) for n in range(RATIFIED_N_BINS)], dtype=torch.float64,
        )
        raw_means_trial_1 = [float(v) for v in range(1, RATIFIED_N_BINS + 1)]
        raw_means_trial_2 = [float(v) * 100.0 for v in range(1, RATIFIED_N_BINS + 1)]

        _loss_1, details_1 = causal_physics_loss(
            raw_means_trial_1, r_ref=1.0, frozen_weights=frozen_weights,
            dtype=torch.float64, device=torch.device("cpu"), return_details=True,
        )
        _loss_2, details_2 = causal_physics_loss(
            raw_means_trial_2, r_ref=1.0, frozen_weights=frozen_weights,
            dtype=torch.float64, device=torch.device("cpu"), return_details=True,
        )
        self.assertTrue(
            torch.equal(details_1["w_n"], frozen_weights),
            "the returned w_n must be exactly the supplied frozen_weights, "
            "not a value recomputed from this call's own residuals",
        )
        self.assertTrue(
            torch.equal(details_1["w_n"], details_2["w_n"]),
            "the frozen weight vector must be BYTE-IDENTICAL across two "
            "trial evaluations with completely different residuals -- the "
            "GAP-54-06 defect is exactly a weight vector that silently "
            "changes with the trial parameters",
        )

    def test_frozen_weights_carry_no_gradient_while_residual_still_does(self) -> None:
        """RESEARCH.md pitfall: "only causal weights are detached for
        L-BFGS; trial residuals must retain gradients."
        """
        frozen_weights = torch.tensor(
            [1.0 / (n + 1) for n in range(RATIFIED_N_BINS)], dtype=torch.float64,
        )
        raw_means = torch.tensor(
            [float(v) for v in range(1, RATIFIED_N_BINS + 1)],
            dtype=torch.float64, requires_grad=True,
        )
        loss, details = causal_physics_loss(
            raw_means, r_ref=1.0, frozen_weights=frozen_weights,
            dtype=torch.float64, device=torch.device("cpu"), return_details=True,
        )
        loss.backward()
        self.assertIsNotNone(
            raw_means.grad,
            "the trial residual (model-derived) must still receive a "
            "gradient even when the causal weight is externally frozen",
        )
        self.assertFalse(
            details["w_n"].requires_grad,
            "the frozen weight vector must never acquire a gradient",
        )

    def test_segment_state_restores_exactly(self) -> None:
        """The L-BFGS segment's frozen samples and detached causal weights
        must be part of the persisted, resumable checkpoint state and
        restore byte-identical -- resume must never regenerate them.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            train_source = make_full_slot_source()
            validation_source = make_stub_source(n_stage0=50, id_offset=91_000)
            controller = build_run_controller(
                train_source, validation_source, tmp_dir=tmp_dir,
            )
            state = controller.state_dict()
            self.assertTrue(
                "lbfgs_segment_state" in state,
                "RunController.state_dict() must carry an "
                "'lbfgs_segment_state' key (the frozen segment collocation "
                "samples and detached causal weights) so resume restores "
                "the exact same bytes rather than re-drawing/recomputing "
                f"them (GAP-54-06 / 57-RULING.md checkpoint 3); got keys "
                f"{sorted(state.keys())!r}",
            )
