"""Phase 57 Task 1/2 — the controller-level amended-recipe production path.

Drives the REAL production seam (``RunController._stage_batch`` ->
``RunController._build_anchor_context`` -> ``RunController._non_data_terms``,
and ``pinn.data.batches.sample_collocation_points`` directly) against
synthetic, dataset-free, held-out-free fixtures. Every test in this module
is expected to be RED against the current implementation because the
ratified §3.2 allocation / normalization contract
(``pinn_architecture.md`` "Phase 56 contract: collocation allocation and
time draw amended"; ``57-RULING.md``) is not yet implemented -- never
because of an import, syntax, fixture, data, or environment error.

D-01/D-02 (57-CONTEXT.md): this is the bounded conformance TARGET, not an
implementation. No production file is edited by this module.
"""

from __future__ import annotations

import inspect
import tempfile
import unittest
from collections import Counter

import numpy as np
import torch

from pinn.data.batches import select_stage_records, sample_collocation_points
from pinn.training.controllers import RunController

from tests.phase57._fixtures import (
    RATIFIED_N_BINS,
    RATIFIED_PER_BIN,
    RATIFIED_TOTAL,
    REPLAY_ONLY_SLOTS,
    bin_counts,
    bin_index_for_time,
    build_run_controller,
    make_full_slot_source,
    make_replay_only_source,
    make_stub_source,
    per_key_row_counts,
)


class ProductionPathContractTests(unittest.TestCase):
    """One real ``RunController`` loss step over the complete amended recipe.

    §3.2 requires the physics term to consume the FULL 4096-row, 16-bin,
    all-selected-slot collocation object (``FixedBatch.collocation_points``)
    -- not a single anchor identity's own small draw from
    ``CollocationSampler.uniform()`` (the current path,
    ``RunController._build_anchor_context`` /
    ``RunController._non_data_terms``; 57-RESEARCH.md "Component and Symbol
    Map").
    """

    def setUp(self) -> None:
        self.train_source = make_full_slot_source()
        self.validation_source = make_stub_source(n_stage0=50, id_offset=90_000)
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        # A deliberately SMALL CollocationSampler point count (2) so a
        # controller still reaching into it -- instead of the batch's 4096
        # rows -- produces an unmistakably wrong bin count, not a
        # coincidentally-correct one.
        self.controller = build_run_controller(
            self.train_source, self.validation_source,
            tmp_dir=self._tmpdir.name, s_h=1.0, n_collocation_sampler_points=2,
        )

    def test_controller_uses_complete_amended_recipe(self) -> None:
        """One real RunController step must emit the complete §3.2 recipe.

        Drives ``_stage_batch`` (DATA-05 real production selection) ->
        ``_build_anchor_context`` -> ``_non_data_terms`` (the real physics
        seam) and asserts the widened diagnostic stash
        (``RunController._last_widened_details``, populated by
        ``causal_physics_loss(..., return_details=True)``) carries:

        * exactly ``RATIFIED_N_BINS`` (16) per-bin residual entries -- the
          batch-global bin means, not a per-anchor per-time residual vector
          sized by ``CollocationSampler``;
        * both RAW and NORMALIZED diagnostics (``raw_residuals_per_bin`` and
          the frozen ``r_ref`` the normalization used) -- 57-RESEARCH.md's
          "Component and Symbol Map" requires the causal loss to "expose
          raw/normalized diagnostics";
        * a finite normalized causal loss.
        """
        batch = self.controller._stage_batch(
            self.train_source, stage=0, collocation_count=RATIFIED_TOTAL,
        )
        self.assertEqual(batch.collocation_points.times.numel(), RATIFIED_TOTAL)

        anchor_ctx = self.controller._build_anchor_context(
            self.train_source, batch, None,
        )
        terms = self.controller._non_data_terms(anchor_ctx)

        details = self.controller._last_widened_details
        self.assertIsNotNone(
            details, "RunController._non_data_terms must populate "
            "_last_widened_details on every call",
        )
        self.assertEqual(
            len(details["residuals_per_bin"]), RATIFIED_N_BINS,
            "the physics residual must be reduced to the ratified 16 "
            "batch-global bin means (pinn_architecture.md Phase-56 "
            "contract), not a per-anchor per-time residual vector sized by "
            "CollocationSampler",
        )
        self.assertIn(
            "raw_residuals_per_bin", details,
            "the widened stash must expose the RAW (un-normalized) bin "
            "means alongside the normalized ones -- 57-RESEARCH.md "
            "'Component and Symbol Map' requires both raw and normalized "
            "diagnostics",
        )
        self.assertIn(
            "r_ref", details,
            "the widened stash must record the frozen R_ref the "
            "normalization used, so raw-unit thresholds are never silently "
            "applied to normalized values",
        )
        self.assertTrue(
            bool(torch.isfinite(terms["phys"])),
            "the normalized causal physics loss must be finite",
        )

    def test_energy_and_angular_momentum_reuse_the_physics_collocation_set(self) -> None:
        """§3.2's re-issued acceptance criterion: energy reuses the physics set.

        ``pinn_architecture.md`` "Phase 56 contract: collocation allocation
        and time draw amended": "This re-ratifies the time allocation only;
        energy continues to reuse the physics set." A source-level pin: the
        SAME ``positions``/``velocities`` local tensors that feed the
        physics residual (``softened_acceleration``) must also feed
        ``soft_energy_loss`` and ``angular_momentum_loss`` -- never a
        second, independently-drawn collocation set for energy/angmom.
        """
        source = inspect.getsource(RunController._non_data_terms)
        self.assertRegex(
            source,
            r"soft_energy_loss\(\s*positions,\s*velocities,",
            "soft_energy_loss must consume the physics term's own "
            "positions/velocities, not a second collocation draw",
        )
        self.assertRegex(
            source,
            r"angular_momentum_loss\(\s*positions,\s*velocities,",
            "angular_momentum_loss must consume the physics term's own "
            "positions/velocities, not a second collocation draw",
        )


class AllocationContractTests(unittest.TestCase):
    """The exact §3.2 selected-slot / bin allocation contract.

    Drives ``pinn.data.batches.sample_collocation_points`` directly (the
    real DATA-05 production seam ``RunController._stage_batch`` delegates
    to) against both the general 256-slot (240 replay + 16 lookahead) shape
    and the real Stage-0-only 240-replay-only shape v2.3 actually trains
    under (no curriculum Stage-1 population exists yet in this milestone).
    """

    def _colloc(self, source, *, seed=0):
        rng = np.random.default_rng(seed)
        selected = select_stage_records(source, stage=0, rng=rng)
        keys = selected.replay + selected.lookahead
        colloc = sample_collocation_points(
            source, keys, rng=rng, dtype=torch.float64, device=torch.device("cpu"),
            collocation_count=RATIFIED_TOTAL,
        )
        return keys, colloc

    def test_full_slot_batch_emits_exactly_256_rows_per_bin(self) -> None:
        """A 256-slot batch must emit exactly RATIFIED_PER_BIN rows in EVERY
        one of the 16 fixed equal-``u`` bins (54-RULING.md "Batch allocation
        and bin policy") -- not a global-uniform draw whose per-bin count is
        merely close to 256 in expectation.
        """
        source = make_full_slot_source()
        _keys, colloc = self._colloc(source)
        self.assertEqual(colloc.times.numel(), RATIFIED_TOTAL)
        counts = bin_counts(colloc.times.tolist())
        self.assertEqual(
            counts, [RATIFIED_PER_BIN] * RATIFIED_N_BINS,
            f"every one of the {RATIFIED_N_BINS} fixed bins must hold "
            f"exactly {RATIFIED_PER_BIN} rows; got {counts}",
        )

    def test_full_slot_batch_every_bin_contains_every_selected_slot_exactly_once(self) -> None:
        """54-RULING.md: "In a 256-slot batch, draw one point per selected
        slot inside every bin." Every one of the 16 bins must therefore
        contain the FULL 256-slot multiset exactly once -- no slot missing,
        none doubled, in any bin.
        """
        source = make_full_slot_source()
        keys, colloc = self._colloc(source)
        times = colloc.times.tolist()
        by_bin: dict = {b: [] for b in range(RATIFIED_N_BINS)}
        for t, key in zip(times, colloc.record_keys):
            by_bin[bin_index_for_time(t)].append(key)
        expected = sorted(keys)
        for bin_id in range(RATIFIED_N_BINS):
            self.assertEqual(
                sorted(by_bin[bin_id]), expected,
                f"bin {bin_id} must contain exactly the 256 selected slots, "
                "each exactly once",
            )

    def test_replay_only_batch_stratifies_256_rows_per_bin(self) -> None:
        """The real Stage-0-only 240-slot (replay-only, no lookahead) shape
        must ALSO stratify to exactly 256 rows per bin -- the ratified
        3840-plus-256-remainder construction (54-RULING.md), not the
        240-slot near-even global-uniform quota the current implementation
        draws.
        """
        source = make_replay_only_source()
        _keys, colloc = self._colloc(source)
        self.assertEqual(colloc.times.numel(), RATIFIED_TOTAL)
        counts = bin_counts(colloc.times.tolist())
        self.assertEqual(
            counts, [RATIFIED_PER_BIN] * RATIFIED_N_BINS,
            f"every one of the {RATIFIED_N_BINS} fixed bins must hold "
            f"exactly {RATIFIED_PER_BIN} rows for the 240-slot replay-only "
            f"batch too; got {counts}",
        )

    def test_replay_only_batch_seventeen_eighteen_multiplicity(self) -> None:
        """54-RULING.md: a replay-only 240-slot batch gives 224 slots exactly
        17 rows and 16 slots exactly 18 rows (the seeded-permutation
        second-draw construction), on top of the per-bin exactness above.

        Note: the CURRENT near-even ``allocate_collocation_quota`` divmod
        already happens to produce a {17, 18} per-slot total split for
        240 slots / 4096 rows by coincidence of the arithmetic
        (``divmod(4096, 240) == (17, 16)``) -- the missing production
        contract this test enforces is the CONJUNCTION with per-bin
        exactness above: the ratified rule ties the extra row to a specific
        bin (via the canonical seeded permutation), not to an
        arbitrarily-bin-scattered global draw.
        """
        source = make_replay_only_source()
        _keys, colloc = self._colloc(source)
        per_key = per_key_row_counts(colloc.record_keys)
        self.assertEqual(len(per_key), REPLAY_ONLY_SLOTS)
        counts = Counter(per_key.values())
        self.assertEqual(
            counts, Counter({17: 224, 18: 16}),
            f"expected 224 slots with 17 rows and 16 slots with 18 rows; "
            f"got {dict(counts)}",
        )
        bin_membership = bin_counts(colloc.times.tolist())
        self.assertEqual(
            bin_membership, [RATIFIED_PER_BIN] * RATIFIED_N_BINS,
            "the 17/18 multiplicity must be realized THROUGH exact "
            "per-bin allocation, not merely as an aggregate per-slot total",
        )

    def test_unsupported_slot_count_fails_closed_rather_than_reducing(self) -> None:
        """A slot count that is neither the ratified 256 (full) nor 240
        (replay-only) shape has no defined near-even-quota construction
        under the ratified §3.2 rule -- the bounded patch must REFUSE
        (fail closed) rather than silently falling back to the legacy
        global-uniform per-slot-quota scheme. 54-RULING.md /
        pinn_architecture.md "Phase 56 contract": "A resource failure ...
        is a fail-closed result, not permission to reduce the count
        silently."
        """
        source = make_stub_source(n_stage0=100, n_stage1=0)
        rng = np.random.default_rng(0)
        selected = select_stage_records(source, stage=0, rng=rng, replay_count=100)
        with self.assertRaises(
            ValueError,
            msg="sample_collocation_points must refuse an out-of-contract "
            "slot count for the ratified 16-bin stratified allocation "
            "rather than silently returning a non-stratified draw",
        ):
            sample_collocation_points(
                source, selected.replay, rng=rng, dtype=torch.float64,
                device=torch.device("cpu"), collocation_count=RATIFIED_TOTAL,
            )


if __name__ == "__main__":
    unittest.main()
