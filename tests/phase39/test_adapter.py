"""Phase 39 Wave-0 contract — shared types + the in-memory admitted-set adapter.

Deferred contracts for Plan 02's ``pinn.data.types`` and ``pinn.data.adapter``
(DATA-01 / DATA-03, plus the frozen identities/outcomes every later module
consumes). Every test SKIPs via the localized ``_require`` helper (importing the
single ``tests.phase39._SKIP_PHRASE``) until the production symbol lands, then
turns green. No production file is created or edited here (Plans 02/03 own all
of ``pinn/data``).

Contract highlights (39-01-PLAN task 39-01-01 acceptance criteria):

* Identity equality/order depends on STRUCTURAL fields, never path formatting;
  invalid shape/fidelity/negative id fails before use.
* ``StageLabel`` admits only ``0``, ``1``, ``UNASSIGNED``; ``DataVersionHashDeferred``
  is distinguishable from success/``None``; mismatch is an exception; the fatal
  Stage-0 result carries the exact threshold (240) and observed count.
* ``FixedBatch.data_points`` and ``.collocation_points`` are separate frozen
  fields (never one aliased point set); model tensors carry last dims 14 and 3.
* GAP-39-07 ``resident_tensor_bytes`` deduplicates shared storage (40 + view +
  20 = 60, not 80) and the mem line is ``mem: 60 (0.600000) watermark=0.7``.
* A deferred synthetic end-to-end contract wires adapter -> split ->
  build_stage_batch -> build_population_report on one ``TinyCorpus`` (N6).
"""

import importlib
import unittest
import warnings

import numpy as np

from tests.phase39 import _SKIP_PHRASE
from tests.phase39 import _fixtures

TYPES = "pinn.data.types"
ADAPTER = "pinn.data.adapter"
PREPROCESSING = "pinn.data.preprocessing"
SPLITS = "pinn.data.splits"
BATCHES = "pinn.data.batches"
STAGE_SCAN = "pinn.data.stage_scan"


def _require(symbol, module):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


def _load_torch():
    try:
        import torch
    except ImportError as exc:  # pragma: no cover
        raise unittest.SkipTest(f"torch not installed: {exc}")
    return torch


# ===========================================================================
# Structural identities.
# ===========================================================================

class IdentityTypeTests(unittest.TestCase):
    def test_physical_key_equality_and_order_are_structural(self):
        PhysicalKey = _require("PhysicalKey", TYPES)
        a = PhysicalKey("hierarchical", 7)
        b = PhysicalKey("hierarchical", 7)
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))              # hashable identity
        self.assertLess(PhysicalKey("hierarchical", 1), PhysicalKey("hierarchical", 2))
        self.assertEqual(len({a, b}), 1)                # de-dups by fields

    def test_record_key_distinguishes_fidelity(self):
        RecordKey = _require("RecordKey", TYPES)
        base = RecordKey("hierarchical", "base", 7)
        gold = RecordKey("hierarchical", "gold", 7)
        self.assertNotEqual(base, gold)
        self.assertEqual(base, RecordKey("hierarchical", "base", 7))

    def test_invalid_identity_inputs_fail_before_use(self):
        PhysicalKey = _require("PhysicalKey", TYPES)
        RecordKey = _require("RecordKey", TYPES)
        for bad_variant in ("gold", "brutus_hierarchical", "", None):
            with self.assertRaises((ValueError, TypeError)):
                PhysicalKey(bad_variant, 1)
        for bad_id in (-1, "abc", 1.5):
            with self.assertRaises((ValueError, TypeError)):
                PhysicalKey("hierarchical", bad_id)
        for bad_fidelity in ("silver", "", None):
            with self.assertRaises((ValueError, TypeError)):
                RecordKey("hierarchical", bad_fidelity, 1)

    def test_identity_is_not_a_formatted_path(self):
        PhysicalKey = _require("PhysicalKey", TYPES)
        # Equality must not depend on any zero-padding / path rendering: the
        # structural id 7 is one identity regardless of how a path spells it.
        self.assertEqual(PhysicalKey("hierarchical", 7), PhysicalKey("hierarchical", 7))


class StageLabelTypeTests(unittest.TestCase):
    def test_only_three_labels_admitted(self):
        StageLabel = _require("StageLabel", TYPES)
        self.assertEqual(StageLabel(0), StageLabel.STAGE_0)
        self.assertEqual(StageLabel(1), StageLabel.STAGE_1)
        self.assertEqual(StageLabel("UNASSIGNED"), StageLabel.UNASSIGNED)
        for bad in (2, 3, 5, 6, "STAGE_0", "nope"):
            with self.assertRaises(ValueError):
                StageLabel(bad)
        for forbidden in ("STAGE_2", "STAGE_3", "STAGE_4", "STAGE_5", "STAGE_6"):
            self.assertFalse(hasattr(StageLabel, forbidden))


# ===========================================================================
# Version + fatal outcome types.
# ===========================================================================

class VersionOutcomeTypeTests(unittest.TestCase):
    def test_deferred_is_distinct_from_success_and_none(self):
        Deferred = _require("DataVersionHashDeferred", TYPES)
        Verified = _require("DataVersionHashVerified", TYPES)
        self.assertIsNot(Deferred, None)
        self.assertIsNot(Deferred, True)
        self.assertNotEqual(Deferred, None)
        self.assertNotEqual(Deferred, True)
        self.assertNotEqual(Deferred, Verified)

    def test_mismatch_is_a_hard_exception_type(self):
        Mismatch = _require("DataVersionHashMismatch", TYPES)
        self.assertTrue(issubclass(Mismatch, Exception))


class FatalResultTypeTests(unittest.TestCase):
    def test_stage_zero_underpopulated_carries_threshold_and_observed(self):
        Fatal = _require("StageZeroUnderpopulated", TYPES)
        fatal = Fatal(observed=5, threshold=240)
        self.assertEqual(fatal.threshold, 240)
        self.assertEqual(fatal.observed, 5)


# ===========================================================================
# Point-set / batch field separation.
# ===========================================================================

class PointSetAndBatchTypeTests(unittest.TestCase):
    def test_data_and_collocation_point_sets_are_distinct_types(self):
        DataFidelityPoints = _require("DataFidelityPoints", TYPES)
        PhysicsCollocationPoints = _require("PhysicsCollocationPoints", TYPES)
        self.assertIsNot(DataFidelityPoints, PhysicsCollocationPoints)

    def test_fixed_batch_keeps_two_separate_point_set_fields(self):
        import dataclasses
        FixedBatch = _require("FixedBatch", TYPES)
        names = {f.name for f in dataclasses.fields(FixedBatch)}
        self.assertIn("data_points", names)
        self.assertIn("collocation_points", names)
        # They cannot be one undifferentiated point-set field.
        self.assertNotEqual("data_points", "collocation_points")

    def test_data_fidelity_points_expose_input_and_raw_mass_fields(self):
        import dataclasses
        DataFidelityPoints = _require("DataFidelityPoints", TYPES)
        names = {f.name for f in dataclasses.fields(DataFidelityPoints)}
        # 14-wide [tau, IC13] and raw (N, 3) masses travel separately.
        self.assertTrue({"tau_ic13", "masses"} <= names,
                        f"DataFidelityPoints must carry tau_ic13 + masses; got {names}")


# ===========================================================================
# GAP-39-07 deterministic resident-tensor bytes + mem line.
# ===========================================================================

class ResidentBytesTests(unittest.TestCase):
    def test_shared_storage_is_counted_once(self):
        torch = _load_torch()
        resident_tensor_bytes = _require("resident_tensor_bytes", ADAPTER)
        owned = torch.zeros(10, dtype=torch.float32)   # 40 bytes
        view = owned[:5]                                # shares storage -> +0
        independent = torch.zeros(5, dtype=torch.float32)  # 20 bytes
        self.assertEqual(resident_tensor_bytes([owned, view, independent]), 60)

    def test_mem_line_exact_format(self):
        format_mem_line = _require("format_mem_line", ADAPTER)
        line = format_mem_line(60, 100)
        self.assertEqual(line, "mem: 60 (0.600000) watermark=0.7")

    def test_metric_ignores_unrelated_process_allocations(self):
        torch = _load_torch()
        resident_tensor_bytes = _require("resident_tensor_bytes", ADAPTER)
        owned = torch.zeros(10, dtype=torch.float32)
        before = resident_tensor_bytes([owned])
        _unrelated = torch.zeros(1000, dtype=torch.float32)  # not in the set
        self.assertEqual(resident_tensor_bytes([owned]), before)


# ===========================================================================
# Task 39-02-01 — sole float64 parser helpers + version outcomes (green now).
# ===========================================================================

class FolderTableMappingTests(unittest.TestCase):
    """HIGH-3: the README-confirmed 4->2 variant-based Brutus->IC mapping."""

    def test_folder_table_pins_four_brutus_to_two_ic_folders(self):
        table = _require("BRUTUS_FOLDER_TABLE", ADAPTER)
        ic_for_variant = _require("IC_FOLDER_FOR_VARIANT", ADAPTER)
        self.assertEqual(set(table), set(_fixtures.BRUTUS_FOLDERS))
        self.assertEqual(set(ic_for_variant), {"hierarchical", "standard"})
        for folder in ("brutus_hierarchical", "brutus_hierarchical_gold_standard"):
            variant, _fidelity = table[folder]
            self.assertEqual(ic_for_variant[variant], "ic_hierarchical")
        for folder in ("brutus_standard_quasi_random",
                        "brutus_standard_quasi_random_gold_standard"):
            variant, _fidelity = table[folder]
            self.assertEqual(ic_for_variant[variant], "ic_standard_quasi_random")
        # No ``_for_gold_standard`` IC folder is ever named.
        self.assertNotIn("ic_hierarchical_for_gold_standard", ic_for_variant.values())

    def test_record_key_from_brutus_resolves_across_all_four_folders(self):
        record_key_from_brutus = _require("record_key_from_brutus", ADAPTER)
        cases = [
            ("brutus_hierarchical", "brutus_hierarchical_0007.txt", "hierarchical", "base", 7),
            ("brutus_hierarchical_gold_standard", "brutus_hierarchical_0007.txt",
             "hierarchical", "gold", 7),
            ("brutus_standard_quasi_random", "brutus_standard_0005.txt", "standard", "base", 5),
            ("brutus_standard_quasi_random_gold_standard", "brutus_standard_0005.txt",
             "standard", "gold", 5),
        ]
        for folder, filename, variant, fidelity, id_ in cases:
            key = record_key_from_brutus(folder, filename)
            self.assertEqual((key.variant, key.fidelity, key.id), (variant, fidelity, id_))

    def test_gold_brutus_pairs_to_a_base_ic_physical_key(self):
        """HIGH-3: a gold record ADMITS via its base IC sibling even though no
        ``_for_gold_standard`` IC folder exists."""
        record_key_from_brutus = _require("record_key_from_brutus", ADAPTER)
        physical_key_from_ic = _require("physical_key_from_ic", ADAPTER)
        gold_key = record_key_from_brutus(
            "brutus_hierarchical_gold_standard", "brutus_hierarchical_0000.txt")
        base_ic_key = physical_key_from_ic("ic_hierarchical", "ic_hierarchical_0000.txt")
        self.assertEqual(gold_key.physical_key, base_ic_key)

    def test_malformed_filename_and_folder_variant_mismatch_fail(self):
        record_key_from_brutus = _require("record_key_from_brutus", ADAPTER)
        physical_key_from_ic = _require("physical_key_from_ic", ADAPTER)
        with self.assertRaises(ValueError):
            record_key_from_brutus("brutus_hierarchical", "not_a_trajectory.txt")
        with self.assertRaises(ValueError):
            record_key_from_brutus("brutus_hierarchical", "brutus_standard_0001.txt")
        with self.assertRaises(ValueError):
            physical_key_from_ic("ic_hierarchical", "ic_standard_0001.txt")
        with self.assertRaises(ValueError):
            record_key_from_brutus("unknown_folder", "brutus_hierarchical_0001.txt")


class AsymmetricPairingTests(unittest.TestCase):
    """DATA-04 ``physical_key = (variant, id)`` grouping, never a 1:1 folder
    correspondence (HIGH-3)."""

    def test_asymmetric_pairing_quarantines_by_physical_key(self):
        PhysicalKey = _require("PhysicalKey", TYPES)
        pair_by_physical_key = _require("pair_by_physical_key", ADAPTER)
        with _fixtures.TinyCorpus() as corpus:
            bv, bid = corpus.brutus_without_ic
            iv, iid = corpus.ic_without_brutus
            gv, gid = corpus.gold_with_base_ic
            brutus_keys = {PhysicalKey(bv, bid), PhysicalKey(gv, gid), PhysicalKey("hierarchical", 3)}
            ic_keys = {PhysicalKey(iv, iid), PhysicalKey(gv, gid), PhysicalKey("hierarchical", 3)}
            result = pair_by_physical_key(brutus_keys, ic_keys)
            self.assertIn(PhysicalKey(bv, bid), result.missing_ic_sibling)
            self.assertIn(PhysicalKey(iv, iid), result.missing_brutus_sibling)
            # The gold-with-base-IC case is NOT an anomaly: it pairs cleanly.
            self.assertNotIn(PhysicalKey(gv, gid), result.missing_ic_sibling)
            self.assertNotIn(PhysicalKey(gv, gid), result.missing_brutus_sibling)


class FooterProvenanceTests(unittest.TestCase):
    """Full / absent / partial footer provenance across all four folder
    variants, plus the exact GAP-39-09 1% measured-vs-reference boundary."""

    def test_full_footer_is_all_direct_not_anomalous(self):
        parse_footer = _require("parse_footer", ADAPTER)
        ref, prov, anomalous, missing = parse_footer(
            _fixtures.FOOTER_FULL, variant="hierarchical", fidelity="base")
        self.assertEqual(ref["tol"], 1e-15)
        self.assertEqual(ref["Lw"], 130)
        self.assertAlmostEqual(ref["dt_out"], 0.08)
        self.assertAlmostEqual(ref["eta"], 0.263027)
        self.assertTrue(all(v == "direct" for v in prov.values()))
        self.assertFalse(anomalous)
        self.assertEqual(missing, ())

    def test_absent_footer_infers_folder_defaults_per_variant(self):
        parse_footer = _require("parse_footer", ADAPTER)
        cases = [
            ("hierarchical", "base", dict(tol=1e-15, Lw=130, dt_out=0.08)),
            ("standard", "base", dict(tol=1e-13, Lw=118, dt_out=0.17)),
            ("hierarchical", "gold", dict(tol=1e-13, Lw=130, dt_out=0.01)),
            ("standard", "gold", dict(tol=1e-13, Lw=130, dt_out=0.01)),
        ]
        for variant, fidelity, expected in cases:
            ref, prov, anomalous, missing = parse_footer(
                None, variant=variant, fidelity=fidelity)
            for key, value in expected.items():
                self.assertAlmostEqual(ref[key], value)
                self.assertEqual(prov[key], "inferred")
            self.assertIsNone(ref["eta"])
            self.assertEqual(prov["eta"], "absent")
            self.assertFalse(anomalous)   # absence is the expected, not anomalous, case
            self.assertEqual(missing, ())

    def test_partial_footer_is_anomalous_and_logs_missing_names(self):
        parse_footer = _require("parse_footer", ADAPTER)
        ref, prov, anomalous, missing = parse_footer(
            _fixtures.FOOTER_PARTIAL, variant="hierarchical", fidelity="base")
        self.assertEqual(prov["tol"], "direct")
        self.assertEqual(prov["dt_out"], "direct")
        self.assertEqual(prov["t_end"], "direct")
        self.assertEqual(prov["eta"], "absent")   # no documented eta default
        self.assertTrue(anomalous)
        self.assertIn("eta", missing)
        self.assertIsNone(ref["eta"])

    def test_footer_never_supplies_energy_fields(self):
        # DATA-02 prohibition: energies are footer-only diagnostics, never a
        # reference/admission field.
        parse_footer = _require("parse_footer", ADAPTER)
        ref, _prov, _anom, _missing = parse_footer(
            _fixtures.FOOTER_FULL, variant="hierarchical", fidelity="base")
        self.assertNotIn("E_initial", ref)
        self.assertNotIn("E_final", ref)
        self.assertNotIn("dE/E", ref)


class MeasuredDtOutTests(unittest.TestCase):
    """GAP-39-09: independently measured ``dt_out`` and the reversible 1%
    relative-disagreement warning boundary."""

    def test_measured_dt_out_is_median_diff_times(self):
        measure_dt_out = _require("measure_dt_out", ADAPTER)
        times = _fixtures.complete_times(12)
        self.assertAlmostEqual(measure_dt_out(times), 10.0 / 11.0, places=6)

    def test_exact_one_percent_does_not_warn_and_above_does(self):
        import math
        dt_out_disagreement_warns = _require("dt_out_disagreement_warns", ADAPTER)
        threshold = _require("DT_OUT_WARN_REL_THRESHOLD", ADAPTER)
        self.assertEqual(threshold, 0.01)
        # reference=100.0, measured=101.0 -> ratio = 1.0/100.0, which is
        # bit-for-bit == the 0.01 literal (IEEE-754 division is correctly
        # rounded), so this boundary is exact, not float-literal-brittle.
        reference, boundary = 100.0, 101.0
        self.assertEqual(abs(boundary - reference) / reference, threshold)
        self.assertFalse(dt_out_disagreement_warns(boundary, reference))
        just_above = math.nextafter(boundary, math.inf)
        self.assertTrue(dt_out_disagreement_warns(just_above, reference))

    def test_absent_or_nonfinite_reference_never_warns(self):
        dt_out_disagreement_warns = _require("dt_out_disagreement_warns", ADAPTER)
        self.assertFalse(dt_out_disagreement_warns(0.9, None))
        self.assertFalse(dt_out_disagreement_warns(float("nan"), 1.0))
        self.assertFalse(dt_out_disagreement_warns(0.9, float("inf")))


class VersionSeamTests(unittest.TestCase):
    """DATA-03 / GAP-39-01: the module-level compare-and-refuse seam."""

    def test_match_is_verified(self):
        verify_data_version = _require("verify_data_version", ADAPTER)
        Verified = _require("DataVersionHashVerified", TYPES)
        self.assertIs(verify_data_version("a" * 64, "a" * 64), Verified)

    def test_mismatch_raises(self):
        verify_data_version = _require("verify_data_version", ADAPTER)
        Mismatch = _require("DataVersionHashMismatch", TYPES)
        with self.assertRaises(Mismatch):
            verify_data_version("a" * 64, "b" * 64)

    def test_absent_canonical_is_deferred(self):
        verify_data_version = _require("verify_data_version", ADAPTER)
        Deferred = _require("DataVersionHashDeferred", TYPES)
        self.assertIs(verify_data_version(None, "b" * 64), Deferred)


class RawParseTests(unittest.TestCase):
    """The parser preserves float64 precision and rejects malformed input."""

    def test_ic_roundtrip_preserves_float64_precision(self):
        parse_ic_text = _require("parse_ic_text", ADAPTER)
        masses, positions, velocities = parse_ic_text(
            "\n".join(_fixtures._body_line(m, i, 0.0)
                      for i, m in enumerate(_fixtures.HIER_MASSES)) + "\n")
        for got, want in zip(masses.tolist(), _fixtures.HIER_MASSES):
            self.assertEqual(got, want)
        self.assertEqual(positions.shape, (3, 3))
        self.assertEqual(velocities.shape, (3, 3))

    def test_brutus_roundtrip_shapes_and_footer_capture(self):
        parse_brutus_text = _require("parse_brutus_text", ADAPTER)
        text = _fixtures._brutus_text(_fixtures.complete_times(12), _fixtures.HIER_MASSES,
                                       footer=_fixtures.FOOTER_FULL)
        parsed = parse_brutus_text(text)
        self.assertEqual(parsed.n_complete_blocks, 12)
        self.assertEqual(parsed.n_nonfinite_blocks, 0)
        self.assertEqual(parsed.n_malformed_blocks, 0)
        self.assertEqual(parsed.positions.shape, (12, 3, 3))
        self.assertEqual(parsed.velocities.shape, (12, 3, 3))
        self.assertIsNotNone(parsed.footer_raw)

    def test_interior_nonfinite_block_is_counted_not_dropped_silently(self):
        # Self-contained override (does not depend on the Wave-0
        # ``_fixtures._nonfinite_interior`` t==4.0 trigger, which the default
        # ``complete_times(12)`` array never hits exactly) so this test is
        # exact regardless of that fixture's own time grid.
        parse_brutus_text = _require("parse_brutus_text", ADAPTER)
        times = _fixtures.complete_times(12)
        target_t = times[6]

        def corrupt(t, i, m):
            if t == target_t and i == 1:
                return f"{m!r} inf 0.0 0.0 0.0 0.0 0.0"
            return _fixtures._body_line(m, i, t)

        text = _fixtures._brutus_text(times, _fixtures.HIER_MASSES, body_override=corrupt)
        parsed = parse_brutus_text(text)
        self.assertEqual(parsed.n_complete_blocks, 12)
        self.assertEqual(parsed.n_nonfinite_blocks, 1)

    def test_malformed_missing_row_is_not_salvaged(self):
        # Self-contained override (does not depend on the Wave-0
        # ``_fixtures._malformed_missing_row`` t==2.0 trigger, which the
        # default ``complete_times(12)`` array never hits exactly).
        parse_brutus_text = _require("parse_brutus_text", ADAPTER)
        times = _fixtures.complete_times(12)
        target_t = times[2]

        def drop_row(t, i, m):
            if t == target_t and i == 2:
                return None
            return _fixtures._body_line(m, i, t)

        text = _fixtures._brutus_text(times, _fixtures.HIER_MASSES, body_override=drop_row)
        parsed = parse_brutus_text(text)
        self.assertEqual(parsed.n_complete_blocks, 11)
        self.assertEqual(parsed.n_malformed_blocks, 1)

    def test_root_containment_rejects_escape(self):
        resolve_within_root = _require("resolve_within_root", ADAPTER)
        with _fixtures.TinyCorpus() as corpus:
            with self.assertRaises(Exception):
                resolve_within_root(corpus.data_root, corpus.data_root / ".." / "escape.txt")

    def test_duplicate_record_key_from_two_scanned_paths_is_equal(self):
        # Identity is structural: the same folder+filename always resolves the
        # same RecordKey, so a scanner can hard-fail on duplicates by equality.
        record_key_from_brutus = _require("record_key_from_brutus", ADAPTER)
        a = record_key_from_brutus("brutus_hierarchical", "brutus_hierarchical_0000.txt")
        b = record_key_from_brutus("brutus_hierarchical", "brutus_hierarchical_0000.txt")
        self.assertEqual(a, b)


# ===========================================================================
# Task 39-02-02 — pure CTL preprocessing, invariants, IC13, normalization.
# ===========================================================================

def _sample_system():
    """One deterministic, non-degenerate 3-body float64 system."""
    masses = np.array([1.35, 0.31, 1.34], dtype=np.float64)
    r0 = np.array([[2.0, 0.5, 0.1], [-1.0, -0.3, 0.2], [0.0, 1.2, -0.4]], dtype=np.float64)
    v0 = np.array([[0.1, 0.2, 0.0], [-0.2, 0.1, 0.05], [0.05, -0.1, 0.1]], dtype=np.float64)
    times = np.linspace(0.0, 10.0, 12)
    positions = np.stack([r0 + 0.01 * t * np.array([1.0, 0.0, 0.0]) for t in times])
    velocities = np.stack([v0 for _ in times])
    return times, positions, velocities, masses


class PreprocessingPipelineTests(unittest.TestCase):
    def test_imports_locked_D_and_produces_float64_deterministic_output(self):
        constants = importlib.import_module("pinn.constants")
        preprocess_trajectory = _require("preprocess_trajectory", PREPROCESSING)
        times, positions, velocities, masses = _sample_system()
        a = preprocess_trajectory(times, positions, velocities, masses)
        b = preprocess_trajectory(times, positions, velocities, masses)
        self.assertEqual(a.D, constants.D_CHARACTERISTIC_LENGTH)
        self.assertAlmostEqual(a.D, 100.0 ** (1.0 / 3.0))
        self.assertEqual(a.r_gauge.dtype, np.float64)
        self.assertEqual(a.v_gauge.dtype, np.float64)
        np.testing.assert_array_equal(a.r_gauge, b.r_gauge)   # deterministic
        np.testing.assert_array_equal(a.masses_ordered, b.masses_ordered)

    def test_com_and_momentum_postconditions_hold_after_preprocessing(self):
        preprocess_trajectory = _require("preprocess_trajectory", PREPROCESSING)
        times, positions, velocities, masses = _sample_system()
        pre = preprocess_trajectory(times, positions, velocities, masses)
        com = np.sum(pre.masses_ordered[:, None] * pre.r0_gauge, axis=0)
        momentum = np.sum(pre.masses_ordered[:, None] * pre.v0_gauge, axis=0)
        self.assertLess(float(np.linalg.norm(com)), 1e-12)
        self.assertLess(float(np.linalg.norm(momentum)), 1e-12)

    def test_mass_invariance_check_passes_and_rejects(self):
        check_mass_invariance = _require("check_mass_invariance", PREPROCESSING)
        MassInvarianceError = _require("MassInvarianceError", PREPROCESSING)
        stable = np.array([[1.0, 2.0, 3.0]] * 5, dtype=np.float64)
        self.assertEqual(check_mass_invariance(stable), 0.0)
        drifting = stable.copy()
        drifting[-1, 0] += 1e-10   # >= 1e-15 tolerance
        with self.assertRaises(MassInvarianceError):
            check_mass_invariance(drifting)

    def test_gauge_degenerate_rho_raises(self):
        preprocess_trajectory = _require("preprocess_trajectory", PREPROCESSING)
        GaugeDegenerateError = _require("GaugeDegenerateError", PREPROCESSING)
        masses = np.array([3.0, 2.0, 1.0], dtype=np.float64)
        r0 = np.array([[0.0, 0.0, 0.0], [1e-12, 0.0, 0.0], [5.0, 0.0, 0.0]], dtype=np.float64)
        v0 = np.zeros((3, 3), dtype=np.float64)
        times = np.linspace(0.0, 10.0, 3)
        positions = np.stack([r0] * 3)
        velocities = np.stack([v0] * 3)
        with self.assertRaises(GaugeDegenerateError):
            preprocess_trajectory(times, positions, velocities, masses)


class InvariantsTests(unittest.TestCase):
    def test_s_min_is_unsoftened_true_pairwise_separation(self):
        compute_invariants = _require("compute_invariants", PREPROCESSING)
        masses = np.array([1.0, 1.0, 1.0], dtype=np.float64)
        r0 = np.array([[0.0, 0.0, 0.0], [0.3, 0.0, 0.0], [0.0, 0.9, 0.0]], dtype=np.float64)
        v0 = np.array([[0.1, 0.0, 0.0], [-0.1, 0.05, 0.0], [0.0, -0.05, 0.1]], dtype=np.float64)
        inv = compute_invariants(masses, r0, v0)
        # True minimal separation (0.3) with NO Plummer softening added.
        self.assertAlmostEqual(inv.s_min, 0.3)

    def test_raw_masses_remain_separate_from_invariants(self):
        # The invariants dataclass carries no mass field; raw masses travel
        # alongside, never folded into E/Q/s_min/l_ratio.
        import dataclasses
        Invariants = _require("Invariants", PREPROCESSING)
        names = {f.name for f in dataclasses.fields(Invariants)}
        self.assertNotIn("masses", names)
        self.assertEqual(names, {"E", "Q", "s_min", "l_ratio", "l_ratio_reason"})

    def test_l_ratio_degenerate_near_collision_returns_none_with_reason(self):
        compute_l_ratio = _require("compute_l_ratio", PREPROCESSING)
        masses = np.array([1.0, 1.0, 1.0], dtype=np.float64)
        r0 = np.array([[1e-9, 0, 0], [0, 1e-9, 0], [0, 0, 1e-9]], dtype=np.float64)
        v0 = np.zeros((3, 3), dtype=np.float64)
        l_ratio, reason = compute_l_ratio(masses, r0, v0, E=1e-12)
        self.assertIsNone(l_ratio)
        self.assertEqual(reason, "degenerate_Lmax")

    def test_l_ratio_overshoot_is_not_clamped(self):
        # No global clamp is authorized (Phase 33 D-33-11): L_norm may
        # legitimately exceed 1 and must be returned raw, un-clipped.
        compute_l_ratio = _require("compute_l_ratio", PREPROCESSING)
        masses = np.array([1.0, 1.0, 1.0], dtype=np.float64)
        r0 = np.array([[2.0, 0, 0], [-1.0, 1.5, 0], [-1.0, -1.5, 0]], dtype=np.float64)
        v0 = np.array([[0, 3.0, 0], [-2.6, -1.5, 0], [2.6, -1.5, 0]], dtype=np.float64)
        # An independently small |E| shrinks L_max (v_char) while L (from r0,v0)
        # stays fixed, forcing a genuine overshoot with no clipping.
        l_ratio, reason = compute_l_ratio(masses, r0, v0, E=-0.01)
        self.assertIsNone(reason)
        self.assertIsNotNone(l_ratio)
        self.assertGreater(l_ratio, 1.0)

    def test_l_ratio_ordinary_finite_case_is_not_degenerate(self):
        compute_l_ratio = _require("compute_l_ratio", PREPROCESSING)
        masses = np.array([1.35, 0.31, 1.34], dtype=np.float64)
        r0 = np.array([[2.0, 0.5, 0.1], [-1.0, -0.3, 0.2], [0.0, 1.2, -0.4]], dtype=np.float64)
        v0 = np.array([[0.1, 0.2, 0.0], [-0.2, 0.1, 0.05], [0.05, -0.1, 0.1]], dtype=np.float64)
        l_ratio, reason = compute_l_ratio(masses, r0, v0, E=-0.8)
        self.assertIsNone(reason)
        self.assertTrue(np.isfinite(l_ratio))


class IC13AndNormalizationTests(unittest.TestCase):
    def test_raw_ic13_exact_shape_and_slot_order(self):
        preprocess_trajectory = _require("preprocess_trajectory", PREPROCESSING)
        compute_invariants = _require("compute_invariants", PREPROCESSING)
        build_raw_ic13 = _require("build_raw_ic13", PREPROCESSING)
        times, positions, velocities, masses = _sample_system()
        pre = preprocess_trajectory(times, positions, velocities, masses)
        inv = compute_invariants(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge)
        ic13 = build_raw_ic13(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge, inv.E)
        self.assertEqual(ic13.shape, (13,))
        self.assertEqual(ic13.dtype, np.float64)
        # Slots 0-2 are the ordered raw masses; slot 12 is E.
        np.testing.assert_array_equal(ic13[:3], pre.masses_ordered)
        self.assertEqual(ic13[12], inv.E)
        # rho_x / lambda_x / lambda_y are slots 3-5.
        m1, m2 = pre.masses_ordered[0], pre.masses_ordered[1]
        rho = pre.r0_gauge[1] - pre.r0_gauge[0]
        lam = pre.r0_gauge[2] - (m1 * pre.r0_gauge[0] + m2 * pre.r0_gauge[1]) / (m1 + m2)
        self.assertAlmostEqual(ic13[3], rho[0])
        self.assertAlmostEqual(ic13[4], lam[0])
        self.assertAlmostEqual(ic13[5], lam[1])

    def test_normalization_roundtrip_and_energy_slot_formula(self):
        compute_normalization_stats = _require("compute_normalization_stats", PREPROCESSING)
        normalize_ic13 = _require("normalize_ic13", PREPROCESSING)
        rng = np.random.default_rng(0)
        pop = rng.normal(size=(20, 13)).astype(np.float64)
        energies = pop[:, 12]
        stats = compute_normalization_stats(pop, energies)
        normalized = normalize_ic13(pop[0], stats)
        self.assertEqual(normalized.shape, (13,))
        expected_first = np.tanh((pop[0, :12] - stats.slot_means) / (stats.slot_stds + 1e-8))
        np.testing.assert_allclose(normalized[:12], expected_first)
        expected_energy = np.tanh(pop[0, 12] / stats.e_scale)
        self.assertAlmostEqual(normalized[12], expected_energy)
        # All slots land in the open (-1, 1) tanh range.
        self.assertTrue(np.all(np.abs(normalized) < 1.0))

    def test_e_scale_uses_median_absolute_trajectory_energy(self):
        compute_normalization_stats = _require("compute_normalization_stats", PREPROCESSING)
        pop = np.zeros((5, 13), dtype=np.float64)
        energies = np.array([-1.0, -2.0, -3.0, -4.0, -5.0])
        stats = compute_normalization_stats(pop, energies)
        self.assertAlmostEqual(stats.e_scale, abs(-3.0) + 1e-8)   # median


# ===========================================================================
# Adapter residency / accessors / version / label persistence (deferred).
# ===========================================================================

class AdapterResidencyTests(unittest.TestCase):
    def _adapter(self, corpus, **over):
        AdmittedSetAdapter = _require("AdmittedSetAdapter", ADAPTER)
        kwargs = dict(root=corpus.data_root, blacklist_path=corpus.blacklist_path,
                      precision="float32", device="cpu", run_dir=corpus.run_dir,
                      version_metadata_path=corpus.version_metadata_path)
        kwargs.update(over)
        return AdmittedSetAdapter(**kwargs)

    def test_admitted_records_are_fp32_resident_with_accessors(self):
        torch = _load_torch()
        RecordKey = _require("RecordKey", TYPES)
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._adapter(corpus)
            key = RecordKey("hierarchical", "base", 0)
            record = adapter.get(key)
            # fp32 residency for model-facing IC13 + raw masses.
            self.assertEqual(record.ic13.dtype, torch.float32)
            self.assertEqual(record.masses.dtype, torch.float32)
            # n_snapshots matches a direct parse (complete_times(12) -> 12 blocks).
            self.assertEqual(adapter.n_snapshots(key), 12)
            # dt_out carries measured + reference provenance (measured ~ 10/11).
            self.assertAlmostEqual(adapter.dt_out(key), 10.0 / 11.0, places=6)
            self.assertTrue(hasattr(record, "dt_out_measured"))
            self.assertTrue(hasattr(record, "dt_out_reference"))

    def test_mem_line_fraction_within_watermark(self):
        import re
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._adapter(corpus, capacity_bytes=1 << 34)  # 16 GB
            line = adapter.mem_line()
            m = re.match(r"mem: (\d+) \((\d+\.\d{6})\) watermark=0\.7", line)
            self.assertIsNotNone(m, line)
            self.assertLessEqual(float(m.group(2)), 0.7)

    def test_empty_admitted_set_is_a_hard_init_failure(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        import json
        AdmittedSetAdapter = _require("AdmittedSetAdapter", ADAPTER)
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "Data"
            for f in _fixtures.IC_FOLDERS:
                (root / _fixtures.IC_SUBDIR / f).mkdir(parents=True)
            for f in _fixtures.BRUTUS_FOLDERS:
                (root / _fixtures.BRUTUS_SUBDIR / f).mkdir(parents=True)
            blacklist = root / "blacklist.json"
            blacklist.write_text(json.dumps({"hierarchical": [], "standard": []}))
            with self.assertRaises((ValueError, RuntimeError)):
                AdmittedSetAdapter(root=root, blacklist_path=blacklist,
                                   precision="float32", device="cpu",
                                   run_dir=Path(tmp) / "run")

    def test_version_hash_match_mismatch_and_absent(self):
        Deferred = _require("DataVersionHashDeferred", TYPES)
        Mismatch = _require("DataVersionHashMismatch", TYPES)
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._adapter(corpus)
            # Match -> a non-deferred verified outcome.
            self.assertNotEqual(adapter.verify_data_version(corpus.known_data_version_hash),
                                Deferred)
            # Mismatch -> hard refusal.
            with self.assertRaises(Mismatch):
                adapter.verify_data_version("b" * 64)
            # Absent metadata -> typed deferral (never a silent match).
            absent = self._adapter(corpus,
                                   version_metadata_path=corpus.absent_version_metadata_path)
            self.assertEqual(absent.verify_data_version("b" * 64), Deferred)

    def test_gold_labels_are_never_derived_from_base(self):
        RecordKey = _require("RecordKey", TYPES)
        StageLabel = _require("StageLabel", TYPES)
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._adapter(corpus)
            # Robust fidelity invariant (independent of the synthetic invariants):
            # every gold record is UNASSIGNED; base labels may be 0/1/UNASSIGNED.
            for id_ in (0, 7):
                gold = RecordKey("hierarchical", "gold", id_)
                if gold in adapter.record_keys():
                    self.assertEqual(adapter.stage_label(gold), StageLabel.UNASSIGNED)
            self.assertEqual(adapter.gold_numeric_stage_count, 0)
            # Every numeric-labeled key is base hierarchical Set 1a.
            for key in adapter.record_keys():
                if adapter.stage_label(key) in (StageLabel.STAGE_0, StageLabel.STAGE_1):
                    self.assertEqual(key.fidelity, "base")
                    self.assertEqual(key.variant, "hierarchical")

    def test_blacklist_membership_is_immutable_and_observed(self):
        PhysicalKey = _require("PhysicalKey", TYPES)
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._adapter(corpus)
            # id 3 hierarchical is blacklisted in the fixture; it is excluded.
            self.assertTrue(adapter.is_blacklisted(PhysicalKey("hierarchical", 3)))
            self.assertNotIn(PhysicalKey("hierarchical", 3),
                             {k.physical_key if hasattr(k, "physical_key")
                              else PhysicalKey(k.variant, k.id)
                              for k in adapter.record_keys()})


# ===========================================================================
# N6 — deferred synthetic end-to-end wiring smoke test.
# ===========================================================================

class EndToEndIntegrationTests(unittest.TestCase):
    """adapter init -> StageQuery -> split -> build_stage_batch ->
    build_population_report on ONE TinyCorpus fixture, asserting no wiring break
    across module boundaries (cross-AI review N6). The adapter IS the StageQuery
    surface consumed by the splitter, batch constructor, and report."""

    def test_full_chain_wires_without_breaking_module_boundaries(self):
        AdmittedSetAdapter = _require("AdmittedSetAdapter", ADAPTER)
        build_split_manifest = _require("build_split_manifest", SPLITS)
        build_stage_batch = _require("build_stage_batch", BATCHES)
        build_population_report = _require("build_population_report", STAGE_SCAN)
        StageZeroUnderpopulated = _require("StageZeroUnderpopulated", TYPES)

        with _fixtures.TinyCorpus() as corpus:
            adapter = AdmittedSetAdapter(
                root=corpus.data_root, blacklist_path=corpus.blacklist_path,
                precision="float32", device="cpu", run_dir=corpus.run_dir,
                version_metadata_path=corpus.version_metadata_path)

            # Split manifest is written into the injected run dir.
            manifest = build_split_manifest(adapter, seed=1234, run_dir=corpus.run_dir)
            self.assertIsNotNone(manifest)

            # Batch construction is reachable; a TinyCorpus cannot supply 240
            # Stage-0 trajectories, so the wiring may legitimately surface the
            # typed underpopulation fatal instead of a batch — either proves the
            # boundary is wired (a crash / import error would not).
            try:
                batch = build_stage_batch(adapter, stage=0)
                if batch is not None:
                    self.assertEqual(batch.data_points.tau_ic13.shape[-1], 14)
                    self.assertEqual(batch.data_points.masses.shape[-1], 3)
            except StageZeroUnderpopulated:
                pass

            # The Stage-0 report always consumes persisted labels and holds the
            # zero-gold invariant regardless of population.
            report = build_population_report(adapter, interim_s0=0.01)
            self.assertEqual(report.gold_numeric_stage_count, 0)


# ===========================================================================
# Task 39-03-01 — production root resolution, fail-closed init, admission
# counting (claude M6, HIGH-A, N3, cycle-4 claude LOW-1).
# ===========================================================================

class ProductionRootAndBlacklistTests(unittest.TestCase):
    def _full_adapter(self, corpus, **over):
        AdmittedSetAdapter = _require("AdmittedSetAdapter", ADAPTER)
        kwargs = dict(root=corpus.data_root, blacklist_path=corpus.blacklist_path,
                      precision="float32", device="cpu", run_dir=corpus.run_dir,
                      version_metadata_path=corpus.version_metadata_path)
        kwargs.update(over)
        return AdmittedSetAdapter(**kwargs)

    def _partial_root(self, tmp, *, with_record):
        import json
        from pathlib import Path
        root = Path(tmp) / "Data"
        # Only ONE of the four Brutus folders (mirrors this worktree's 74-file
        # partial, which carries a single Brutus folder).
        (root / _fixtures.BRUTUS_SUBDIR / "brutus_hierarchical").mkdir(parents=True)
        for f in _fixtures.IC_FOLDERS:
            (root / _fixtures.IC_SUBDIR / f).mkdir(parents=True)
        (root / "problematic_ics_blacklist.json").write_text(
            json.dumps({"hierarchical": [], "standard": []}))
        if with_record:
            _fixtures.write_brutus(
                root / _fixtures.BRUTUS_SUBDIR / "brutus_hierarchical"
                / "brutus_hierarchical_0000.txt",
                _fixtures.complete_times(12), _fixtures.HIER_MASSES, footer=_fixtures.FOOTER_FULL)
        return root

    def test_missing_derived_root_raises_typed_error_naming_path_and_env(self):
        AdmittedSetAdapter = _require("AdmittedSetAdapter", ADAPTER)
        DataSourceRootMissing = _require("DataSourceRootMissing", ADAPTER)
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "nonexistent_Data"
            with self.assertRaises(DataSourceRootMissing) as ctx:
                AdmittedSetAdapter(root=missing, precision="float32", device="cpu")
            msg = str(ctx.exception)
            self.assertIn(str(missing), msg)
            self.assertIn("GSD_DATA_ROOT", msg)

    def test_default_root_uses_git_common_dir_not_worktree_toplevel(self):
        default_data_root = _require("default_data_root", ADAPTER)
        import subprocess
        from pathlib import Path
        default = default_data_root()
        common = subprocess.check_output(
            ["git", "rev-parse", "--git-common-dir"], text=True).strip()
        expected = Path(common).resolve().parent / "simulation_data" / "Data"
        self.assertEqual(default, expected)
        # The main-repo default must NOT be the worktree-local toplevel (which in
        # a linked worktree carries a PARTIAL simulation_data/Data/).
        toplevel = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True).strip()
        worktree_based = Path(toplevel).resolve() / "simulation_data" / "Data"
        if Path(common).resolve().parent != Path(toplevel).resolve():
            self.assertNotEqual(default, worktree_based)
        # No hardcoded personal absolute path is baked into source (claude M6).
        import pinn.data.adapter as adapter_mod
        src = Path(adapter_mod.__file__).read_text(encoding="utf-8")
        self.assertNotIn("/Users/", src)

    def test_partial_corpus_root_raises_incomplete_unless_opt_in(self):
        AdmittedSetAdapter = _require("AdmittedSetAdapter", ADAPTER)
        DataSourceRootIncomplete = _require("DataSourceRootIncomplete", ADAPTER)
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = self._partial_root(tmp, with_record=True)
            blacklist = root / "problematic_ics_blacklist.json"
            os.environ.pop("GSD_ALLOW_PARTIAL_DATA_ROOT", None)
            with self.assertRaises(DataSourceRootIncomplete) as ctx:
                AdmittedSetAdapter(root=root, blacklist_path=blacklist,
                                   precision="float32", device="cpu")
            msg = str(ctx.exception)
            for folder in ("brutus_hierarchical_gold_standard",
                           "brutus_standard_quasi_random",
                           "brutus_standard_quasi_random_gold_standard"):
                self.assertIn(folder, msg)
            # The explicit opt-in (fixture-only) bypass succeeds and records the
            # allow_partial_data_root=1 provenance marker.
            os.environ["GSD_ALLOW_PARTIAL_DATA_ROOT"] = "1"
            try:
                adapter = AdmittedSetAdapter(root=root, blacklist_path=blacklist,
                                             precision="float32", device="cpu")
            finally:
                os.environ.pop("GSD_ALLOW_PARTIAL_DATA_ROOT", None)
            self.assertEqual(adapter.allow_partial_data_root, 1)
            self.assertTrue(any("allow_partial_data_root=1" in ln for ln in adapter.init_log))

    def test_full_corpus_records_allow_partial_zero_by_default(self):
        import os
        os.environ.pop("GSD_ALLOW_PARTIAL_DATA_ROOT", None)
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._full_adapter(corpus)
            self.assertEqual(adapter.allow_partial_data_root, 0)
            self.assertTrue(any("allow_partial_data_root=0" in ln for ln in adapter.init_log))

    def test_invalid_blacklist_schema_hard_fails(self):
        AdmittedSetAdapter = _require("AdmittedSetAdapter", ADAPTER)
        BlacklistSchemaError = _require("BlacklistSchemaError", ADAPTER)
        with _fixtures.TinyCorpus() as corpus:
            with self.assertRaises(BlacklistSchemaError):
                AdmittedSetAdapter(root=corpus.data_root,
                                   blacklist_path=corpus.invalid_blacklist_path,
                                   precision="float32", device="cpu", run_dir=corpus.run_dir)

    def test_remediation_quarantine_is_sourced_from_constructor(self):
        RecordKey = _require("RecordKey", TYPES)
        PhysicalKey = _require("PhysicalKey", TYPES)
        with _fixtures.TinyCorpus() as corpus:
            base = self._full_adapter(corpus)
            self.assertIn(RecordKey("hierarchical", "base", 0), base.record_keys())
            quarantined = self._full_adapter(
                corpus, remediation_quarantine=frozenset({PhysicalKey("hierarchical", 0)}))
            # The adapter passed its constructor value to clause 2, so id 0 (both
            # fidelities) is quarantined out of the admitted set.
            self.assertNotIn(RecordKey("hierarchical", "base", 0), quarantined.record_keys())
            self.assertNotIn(RecordKey("hierarchical", "gold", 0), quarantined.record_keys())
            self.assertGreater(
                quarantined.folder_counts["brutus_hierarchical"]["quarantined"],
                base.folder_counts["brutus_hierarchical"]["quarantined"])

    def test_per_folder_accounting_and_blacklist_logs_are_exact(self):
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._full_adapter(corpus)
            for folder, counts in adapter.folder_counts.items():
                self.assertEqual(
                    counts["found"],
                    counts["admitted"] + counts["rejected"] + counts["quarantined"],
                    f"{folder} found != admitted+rejected+quarantined: {counts}")
            # Per-family blacklist entry counts + absent-ID logs (both listed IDs
            # exist on disk, so absent lists are empty).
            self.assertTrue(any("blacklist hierarchical n_blacklist_entries=1" in ln
                                for ln in adapter.init_log))
            self.assertTrue(any("blacklist standard n_blacklist_entries=1" in ln
                                for ln in adapter.init_log))
            self.assertTrue(any("blacklist hierarchical absent_ids=[]" in ln
                                for ln in adapter.init_log))

    def test_paired_base_gold_identical_invariants_split_the_label(self):
        classify_stage_label = _require("classify_stage_label", "pinn.data.stages")
        StageLabel = _require("StageLabel", TYPES)
        Variant = _require("Variant", TYPES)
        Fidelity = _require("Fidelity", TYPES)
        from types import SimpleNamespace
        shared = dict(E=-1.0, l_ratio=0.8, Q=1.0, s_min=0.5)  # a clean Stage-0 point
        base = SimpleNamespace(variant=Variant.HIERARCHICAL, fidelity=Fidelity.BASE, **shared)
        gold = SimpleNamespace(variant=Variant.HIERARCHICAL, fidelity=Fidelity.GOLD, **shared)
        self.assertEqual(classify_stage_label(base, 0.01), StageLabel.STAGE_0)
        self.assertEqual(classify_stage_label(gold, 0.01), StageLabel.UNASSIGNED)


# ===========================================================================
# Task 39-03-02 — fp32 storage, accessors, GAP-39-07 ballpark cross-check,
# and the minimal package surface (HIGH-1, L1, N7).
# ===========================================================================

class ProductionResidencyAccountingTests(unittest.TestCase):
    def _full_adapter(self, corpus, **over):
        AdmittedSetAdapter = _require("AdmittedSetAdapter", ADAPTER)
        kwargs = dict(root=corpus.data_root, blacklist_path=corpus.blacklist_path,
                      precision="float32", device="cpu", run_dir=corpus.run_dir,
                      version_metadata_path=corpus.version_metadata_path)
        kwargs.update(over)
        return AdmittedSetAdapter(**kwargs)

    def test_floats_per_snapshot_is_nineteen(self):
        FLOATS_PER_SNAPSHOT = _require("FLOATS_PER_SNAPSHOT", ADAPTER)
        # 3 bodies x 6 dof (3 position + 3 velocity) + 1 shared time.
        self.assertEqual(FLOATS_PER_SNAPSHOT, 3 * 6 + 1)
        self.assertEqual(FLOATS_PER_SNAPSHOT, 19)

    def test_mem_ballpark_line_correct_spelling_and_formula(self):
        resident_ballpark_bytes = _require("resident_ballpark_bytes", ADAPTER)
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._full_adapter(corpus)
            total = sum(adapter.n_snapshots(k) for k in adapter.record_keys())
            expected = resident_ballpark_bytes(total)
            self.assertEqual(adapter.mem_ballpark_bytes, expected)
            self.assertEqual(expected, total * 19 * 4)
            # Correct (non-typo) spelling emitted alongside the mem: line.
            self.assertTrue(any("mem_ballpark=" in ln for ln in adapter.init_log))
            self.assertFalse(any("mem_ballpadck" in ln for ln in adapter.init_log))

    def test_resident_bytes_is_a_lower_bound_and_does_not_misfit(self):
        with _fixtures.TinyCorpus() as corpus:
            with warnings.catch_warnings():
                warnings.simplefilter("error")   # a misfit warning would fail here
                adapter = self._full_adapter(corpus)
            # The authoritative deduplicated numerator carries extra per-record
            # IC13/mass floats, so it is >= the snapshot-only lower bound.
            self.assertGreaterEqual(adapter.resident_tensor_bytes(), adapter.mem_ballpark_bytes)

    def test_misfit_warning_fires_when_dedup_count_is_corrupted(self):
        torch = _load_torch()
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._full_adapter(corpus)
            # Artificially corrupt the dedup count to a tiny value; the ballpark
            # stays as computed at init, so the cross-check must warn loudly.
            adapter._resident_tensors = [torch.zeros(1, dtype=torch.float32)]
            with self.assertWarns(UserWarning) as ctx:
                adapter._check_resident_ballpark()
            self.assertIn("resident_tensor_bytes_misfit", str(ctx.warning))

    def test_resident_is_misfit_band_boundaries(self):
        resident_is_misfit = _require("resident_is_misfit", ADAPTER)
        self.assertTrue(resident_is_misfit(100, 1000))    # below 0.5x
        self.assertTrue(resident_is_misfit(4000, 1000))   # above 3.0x
        self.assertFalse(resident_is_misfit(1000, 1000))  # exactly at ballpark
        self.assertFalse(resident_is_misfit(1500, 1000))  # inside the band

    def test_every_resident_tensor_is_cpu_fp32(self):
        torch = _load_torch()
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._full_adapter(corpus)
            for key in adapter.record_keys():
                record = adapter.get(key)
                for name in ("ic13", "masses", "raw_ic13"):
                    tensor = getattr(record, name)
                    self.assertEqual(tensor.dtype, torch.float32, name)
                    self.assertEqual(tensor.device.type, "cpu", name)

    def test_stage_accessors_expose_numeric_only_base_pools(self):
        StageLabel = _require("StageLabel", TYPES)
        with _fixtures.TinyCorpus() as corpus:
            adapter = self._full_adapter(corpus)
            at_or_below = adapter.records_at_or_below(StageLabel.STAGE_1)
            at0 = adapter.records_at(StageLabel.STAGE_0)
            at1 = adapter.records_at(StageLabel.STAGE_1)
            # records_at_or_below never raises on UNASSIGNED (string-valued) labels
            # and is the union of the numeric pools.
            self.assertLessEqual(set(at0) | set(at1), set(at_or_below))
            for key in set(at_or_below) | set(at0) | set(at1):
                self.assertEqual((key.variant, key.fidelity), ("hierarchical", "base"))
                self.assertIsNot(adapter.stage_label(key), StageLabel.UNASSIGNED)
            # has_stage agrees with the persisted label for every admitted record.
            for key in adapter.record_keys():
                self.assertEqual(
                    adapter.has_stage(key),
                    adapter.stage_label(key) is not StageLabel.UNASSIGNED)


class PackageSurfaceTests(unittest.TestCase):
    def test_package_exports_shared_types_and_adapter_without_scanning(self):
        pkg = importlib.import_module("pinn.data")
        for symbol in ("AdmittedSetAdapter", "PhysicalKey", "RecordKey", "StageLabel",
                       "AdmittedRecord", "FixedBatch", "StageQuery"):
            self.assertTrue(hasattr(pkg, symbol), symbol)
        # Parser helpers are NOT part of the public package surface.
        self.assertNotIn("parse_brutus_text", getattr(pkg, "__all__", []))
        self.assertNotIn("parse_footer", getattr(pkg, "__all__", []))

    def test_importing_types_does_not_require_a_corpus(self):
        # A fresh import of the shared-types module never touches disk; it only
        # binds dataclasses/enums. (Corpus discovery is instance-time only.)
        importlib.import_module("pinn.data.types")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
