"""57-07 band-generation-2 Decision A -- mandatory blocking equivalence test.

Proves the memory-bounded microbatched two-pass Adam step
(``RunController._run_adam_step_microbatched``) produces the identical loss
and parameter gradient as the monolithic ``_compose_loss_terms`` + single
``total.backward()`` path, to float tolerance, across microbatch sizes that
do and do not evenly divide the collocation batch -- the 2026-09-09
band-generation-2 scope brief §1.2 requirement. This is the check that
converts Decision A's linearity argument into a verified claim rather than
an assertion; it is a required gate before the microbatched path may be
used for a graded band-generation-2 run.
"""

from __future__ import annotations

import tempfile
import unittest

import torch

from tests.phase40.test_optimizer_phase import _build_controller


class MicrobatchEquivalenceTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def _run_case(self, *, collocation_count, microbatch_sizes):
        for microbatch_size in microbatch_sizes:
            with self.subTest(
                collocation_count=collocation_count, microbatch_size=microbatch_size,
            ):
                controller = _build_controller(
                    self._tmpdir.name, max_epochs=1, n_adam=1,
                    collocation_count=collocation_count,
                )
                parameters = tuple(
                    p for p in controller._model.parameters() if p.requires_grad
                )
                batch = controller._stage_batch(
                    controller._train_source, stage=0,
                    collocation_count=collocation_count,
                )
                anchor_ctx = controller._build_anchor_context(
                    controller._train_source, batch, None,
                )
                weights = controller._scheduled_weights.current(0)

                # Monolithic reference: the pre-57-07 compose-then-backward path.
                for p in parameters:
                    p.grad = None
                mono_terms = controller._compose_loss_terms(batch, anchor_ctx, weights)
                mono_terms.total.backward()
                mono_grads = [
                    p.grad.detach().clone() if p.grad is not None else None
                    for p in parameters
                ]

                # Microbatched candidate: fresh grads, the SAME batch/anchor/weights.
                for p in parameters:
                    p.grad = None
                micro_terms, _gradient_stats = controller._run_adam_step_microbatched(
                    batch, anchor_ctx, weights, parameters,
                    microbatch_size=microbatch_size, want_diagnostics=False,
                )
                micro_grads = [
                    p.grad.detach().clone() if p.grad is not None else None
                    for p in parameters
                ]

                for name, mval, gval in (
                    ("total", mono_terms.total, micro_terms.total),
                    ("data", mono_terms.data, micro_terms.data),
                    ("ic", mono_terms.ic, micro_terms.ic),
                    ("phys", mono_terms.phys, micro_terms.phys),
                    ("energy", mono_terms.energy, micro_terms.energy),
                    ("angmom", mono_terms.angmom, micro_terms.angmom),
                ):
                    self.assertTrue(
                        torch.allclose(mval, gval, rtol=1e-6, atol=1e-9),
                        f"{name} mismatch at collocation_count={collocation_count} "
                        f"microbatch_size={microbatch_size}: "
                        f"monolithic={float(mval.detach())!r} "
                        f"microbatched={float(gval.detach())!r}",
                    )
                self.assertEqual(len(mono_grads), len(micro_grads))
                for i, (mono_g, micro_g) in enumerate(zip(mono_grads, micro_grads)):
                    if mono_g is None and micro_g is None:
                        continue
                    self.assertIsNotNone(
                        mono_g,
                        f"param[{i}] monolithic grad is None but microbatched is not "
                        f"at microbatch_size={microbatch_size}",
                    )
                    self.assertIsNotNone(
                        micro_g,
                        f"param[{i}] microbatched grad is None but monolithic is not "
                        f"at microbatch_size={microbatch_size}",
                    )
                    self.assertTrue(
                        torch.allclose(mono_g, micro_g, rtol=1e-5, atol=1e-8),
                        f"param[{i}] gradient mismatch at "
                        f"collocation_count={collocation_count} "
                        f"microbatch_size={microbatch_size}: "
                        f"max abs diff={float((mono_g - micro_g).abs().max())!r}",
                    )

    def test_equivalence_at_small_scale_including_non_dividing_microbatch(self):
        """Fast check: a 64-row batch at sizes 8 (divides), 20 (does not
        divide), and 64 (single chunk, the degenerate case)."""
        self._run_case(collocation_count=64, microbatch_sizes=[8, 20, 64])

    def test_equivalence_at_ratified_scale_default_microbatch(self):
        """Production-scale check: the ratified 4096-row/16-bin batch at the
        shipped default microbatch size (256, one bin) -- the exact
        configuration band generation 2 will run under."""
        self._run_case(collocation_count=4096, microbatch_sizes=[256])


class GuardFidelityTests(unittest.TestCase):
    """Decision B §2.2: the combined ``grad_norm`` the guard reads must not
    weaken when the five-term diagnostic breakdown is cadence-skipped --
    ``clip_outcome.total_norm`` comes from ``.grad`` after backward, which is
    independent of whether the diagnostic ``autograd.grad`` calls ran."""

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)

    def test_grad_norm_identical_with_and_without_diagnostics(self):
        controller = _build_controller(
            self._tmpdir.name, max_epochs=1, n_adam=1, collocation_count=64,
        )
        parameters = tuple(
            p for p in controller._model.parameters() if p.requires_grad
        )
        batch = controller._stage_batch(
            controller._train_source, stage=0, collocation_count=64,
        )
        anchor_ctx = controller._build_anchor_context(
            controller._train_source, batch, None,
        )
        weights = controller._scheduled_weights.current(0)

        for p in parameters:
            p.grad = None
        _terms_a, stats_a = controller._run_adam_step_microbatched(
            batch, anchor_ctx, weights, parameters,
            microbatch_size=20, want_diagnostics=True,
        )
        norm_a = float(
            controller._grad_clipper.clip(controller._model.parameters(), stage=0).total_norm
        )
        self.assertTrue(stats_a["grad_stats_complete"])

        for p in parameters:
            p.grad = None
        _terms_b, stats_b = controller._run_adam_step_microbatched(
            batch, anchor_ctx, weights, parameters,
            microbatch_size=20, want_diagnostics=False,
        )
        norm_b = float(
            controller._grad_clipper.clip(controller._model.parameters(), stage=0).total_norm
        )
        self.assertFalse(stats_b["grad_stats_complete"])
        for name, _weight_name in (
            ("data", None), ("ic", None), ("phys", None),
            ("energy", None), ("angmom", None),
        ):
            self.assertIsNone(stats_b[f"grad_norm_raw_{name}"])
            self.assertIsNone(stats_b[f"grad_norm_applied_{name}"])

        self.assertAlmostEqual(norm_a, norm_b, places=9)


if __name__ == "__main__":
    unittest.main()
