"""Dataset-free CONF-01 evidence-layer suite (plan 46-04, Tasks 1-2).

Drives the plan-46-04 additions to ``pinn/verification/target_frame_probe.py``:
manifest-parametric population resolution (``resolve_probe_population``), the
deterministic D-05 evidence payload (``render_evidence_payload``), the
containment-guarded evidence writer (``write_frame_probe_evidence``), and the
``python -m pinn.verification.target_frame_probe`` CLI surface. No real-corpus
file is read anywhere in this module (D-24); the single real invocation belongs
to plan 46-06. Every manifest, reader, and outcome below is synthetic.
"""

from __future__ import annotations

import dataclasses
import inspect
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

from pinn.data.adapter import CorpusPathEscape
from pinn.data.preprocessing import preprocess_trajectory
from pinn.data.types import PhysicalKey, RecordKey
from pinn.verification import target_frame_probe as tfp
from pinn.verification.target_frame_probe import (
    ARM_POSITIVE_CONTROL,
    ARM_PROVENANCE_CONTROL,
    ARM_RAW,
    ARM_SCALED,
    VERDICT_AMBIGUOUS,
    VERDICT_TARGETS_ARE_SCALED,
    FrameProbeUnavailable,
)

from tests.phase46._fixtures import make_dual_frame_trajectory, make_stub_split_sources


# ---------------------------------------------------------------------------
# Builders shared across the suite
# ---------------------------------------------------------------------------


def _key(i):
    return RecordKey("hierarchical", "base", int(i))


def _pkey(i):
    return PhysicalKey("hierarchical", int(i))


def _fp32(array):
    return np.asarray(array, dtype=np.float64).astype(np.float32).astype(np.float64)


def _provenance(**overrides):
    fields = dict(
        repo_commit="0" * 40,
        manifests=(
            tfp.ManifestIdentity(
                label="seed42",
                path="configs/splits-seed42.json",
                sha256="a" * 64,
            ),
        ),
        blacklist_sha256="b" * 64,
        data_root_source="explicit",
        dtype="float32",
        device="cpu",
        math="float64",
        torch_version="2.12.0",
        probe_invocation=(
            "python", "-m", "pinn.verification.target_frame_probe",
            "--manifest", "configs/splits-seed42.json",
        ),
    )
    fields.update(overrides)
    return tfp.EvidenceProvenance(**fields)


class _TmpDirMixin:
    def setUp(self):
        self._tmp_ctx = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_ctx.name)

    def tearDown(self):
        self._tmp_ctx.cleanup()


# ---------------------------------------------------------------------------
# Task 1: population resolution (D-02) + reader builders
# ---------------------------------------------------------------------------


class ResolveProbePopulationTest(unittest.TestCase):
    """Task 1 behaviors 1-4: the manifest-parametric eligibility rule."""

    def test_1_eligibility_rule_with_exclusion_attribution(self):
        k = {i: _key(i) for i in range(6)}
        views = {
            "m1": {"train": (k[0], k[1], k[3]), "validation": (k[2], k[4])},
            "m2": {"train": (k[0],), "validation": (k[1], k[2], k[4])},
        }
        test_keys = {"m1": frozenset({_pkey(5)}), "m2": frozenset({_pkey(3)})}
        population = tfp.resolve_probe_population(views, test_keys)
        # train-in-both eligible; validation-in-both eligible; a key
        # train-in-one + validation-in-the-other is eligible with membership
        # recorded per manifest.
        self.assertEqual(population.eligible, (k[0], k[1], k[2], k[4]))
        self.assertEqual(population.membership[k[0]],
                         {"m1": "train", "m2": "train"})
        self.assertEqual(population.membership[k[1]],
                         {"m1": "train", "m2": "validation"})
        self.assertEqual(population.membership[k[2]],
                         {"m1": "validation", "m2": "validation"})
        # train-in-m1 + test-in-m2 -> excluded, attributed to m2.
        self.assertEqual(population.exclusion_ledger["test_under_m2"], (_pkey(3),))
        # test-in-m1 (in no train/validation view) -> excluded, attributed to m1.
        self.assertEqual(population.exclusion_ledger["test_under_m1"], (_pkey(5),))
        self.assertEqual(set(population.exclusion_ledger),
                         {"test_under_m1", "test_under_m2"})
        # Per-manifest per-split counts over the eligible set.
        self.assertEqual(population.counts_per_split_per_manifest["m1"],
                         {"train": 2, "validation": 2})
        self.assertEqual(population.counts_per_split_per_manifest["m2"],
                         {"train": 1, "validation": 3})
        self.assertEqual(population.first_manifest_label, "m1")

    def test_2_single_manifest_degenerates_to_train_plus_validation(self):
        k = {i: _key(i) for i in range(5)}
        views = {"only": {"train": (k[0], k[1]), "validation": (k[2],)}}
        test_keys = {"only": frozenset({_pkey(3), _pkey(4)})}
        population = tfp.resolve_probe_population(views, test_keys)
        self.assertEqual(population.eligible, (k[0], k[1], k[2]))
        # The excluded set is EXACTLY the manifest's test physical keys.
        self.assertEqual(population.exclusion_ledger,
                         {"test_under_only": (_pkey(3), _pkey(4))})
        self.assertEqual(population.counts_per_split_per_manifest["only"],
                         {"train": 2, "validation": 1})

    def test_3_population_structure_exposes_no_withheld_view(self):
        k = {i: _key(i) for i in range(3)}
        views = {"only": {"train": (k[0],), "validation": (k[1],)}}
        population = tfp.resolve_probe_population(
            views, {"only": frozenset({_pkey(2)})})
        field_names = {field.name for field in dataclasses.fields(population)}
        self.assertEqual(
            field_names,
            {"eligible", "membership", "counts_per_split_per_manifest",
             "exclusion_ledger", "first_manifest_label"},
        )
        # Memberships name only train/validation; exclusions are physical keys
        # (read from the manifest payload), never a StageIndex view object.
        split_names = {split for per_key in population.membership.values()
                       for split in per_key.values()}
        self.assertLessEqual(split_names, {"train", "validation"})
        for keys in population.exclusion_ledger.values():
            for physical_key in keys:
                self.assertIsInstance(physical_key, PhysicalKey)

    def test_4_empty_eligibility_raises_unavailable(self):
        k = {i: _key(i) for i in range(2)}
        views = {"only": {"train": (k[0],), "validation": (k[1],)}}
        # Every view key is also in the test partition -> empty eligibility.
        test_keys = {"only": frozenset({_pkey(0), _pkey(1)})}
        with self.assertRaises(FrameProbeUnavailable):
            tfp.resolve_probe_population(views, test_keys)
        with self.assertRaises(FrameProbeUnavailable):
            tfp.resolve_probe_population(
                {"only": {"train": (), "validation": ()}}, {"only": frozenset()})


class ReaderBuildersTest(_TmpDirMixin, unittest.TestCase):
    """Task 1 reader builders: signature/routing/containment coverage here; the
    real-corpus path is exercised by plan 46-06's single run."""

    def test_5_resident_reader_routes_by_membership_and_returns_model_surface(self):
        train_source, validation_source = make_stub_split_sources(
            n_train=2, n_validation=2, n_snapshots=8)
        train_key = train_source.record_keys()[0]
        validation_key = validation_source.record_keys()[0]
        membership = {train_key: "train", validation_key: "validation"}
        reader = tfp._build_resident_reader(
            train_source, validation_source, membership)
        resident = reader(train_key)
        # (times, positions, velocities, masses, ic13) — the model-facing seam.
        self.assertEqual(len(resident), 5)
        times, positions, velocities, masses, ic13 = resident
        np.testing.assert_array_equal(
            np.asarray(times), np.asarray(train_source.snapshot_times(train_key)))
        np.testing.assert_array_equal(
            np.asarray(positions),
            np.asarray(train_source.snapshot_positions(train_key)))
        np.testing.assert_array_equal(
            np.asarray(velocities),
            np.asarray(train_source.snapshot_velocities(train_key)))
        record = train_source.get(train_key)
        self.assertIs(masses, record.masses)
        self.assertIs(ic13, record.ic13)
        # A validation-member key routes to the validation view.
        other = reader(validation_key)
        np.testing.assert_array_equal(
            np.asarray(other[0]),
            np.asarray(validation_source.snapshot_times(validation_key)))
        # Signatures are the CLI contract (chunk_size keyword-only).
        self.assertEqual(
            list(inspect.signature(tfp._build_resident_reader).parameters),
            ["train_index", "validation_index", "membership"])
        self.assertEqual(
            list(inspect.signature(tfp._build_control_reader).parameters),
            ["data_root", "eligible_physical_keys", "chunk_size"])

    def test_6_control_reader_containment_and_eligibility_filtering(self):
        corpus = self.tmp / "corpus"
        folder = corpus / "brutus_output" / "brutus_hierarchical"
        folder.mkdir(parents=True)
        # A symlinked corpus file escaping the root trips the adapter's own
        # containment enforcement inside parse_brutus_file (resolve_within_root).
        outside = self.tmp / "outside.txt"
        outside.write_text("0.0 1 0.0\n", encoding="utf-8")
        (folder / "brutus_hierarchical_0001.txt").symlink_to(outside)
        reader = tfp._build_control_reader(
            corpus, frozenset({_pkey(1)}), chunk_size=4)
        with self.assertRaises(CorpusPathEscape):
            reader(_key(1))
        # A file whose key is NOT eligible is never indexed for parsing.
        (folder / "brutus_hierarchical_0002.txt").write_text(
            "0.0 1 0.0\n", encoding="utf-8")
        reader2 = tfp._build_control_reader(
            corpus, frozenset({_pkey(1)}), chunk_size=4)
        with self.assertRaises(KeyError):
            reader2(_key(2))


# ---------------------------------------------------------------------------
# Task 2: deterministic D-05 evidence + CLI surface
# ---------------------------------------------------------------------------


class EvidencePayloadTest(_TmpDirMixin, unittest.TestCase):
    """Task 2 behaviors 1-5: determinism, D-05 completeness, redaction,
    containment, and non-finite sentinels."""

    @classmethod
    def setUpClass(cls):
        cls.traj = make_dual_frame_trajectory()
        cls.pre = preprocess_trajectory(
            cls.traj.times_raw, cls.traj.positions_raw,
            cls.traj.velocities_raw, cls.traj.masses)
        cls.controls = (cls.traj.times_raw, cls.traj.positions_raw,
                        cls.traj.velocities_raw, cls.traj.masses, cls.pre)
        cls.scaled_resident = (cls.traj.times_raw, _fp32(cls.pre.r_gauge),
                               _fp32(cls.pre.v_gauge), cls.pre.masses_ordered)

    def _run_and_payload(self, residents, provenance=None):
        keys = (_key(1000), _key(1001))
        views = {"seed42": {"train": (keys[0],), "validation": (keys[1],)}}
        test_keys = {"seed42": frozenset({_pkey(1002)})}
        population = tfp.resolve_probe_population(views, test_keys)
        res_book = dict(zip(keys, residents))
        ctrl_book = {key: self.controls for key in keys}
        results, accounting = tfp.probe_population(
            [(key, population.membership[key]) for key in population.eligible],
            lambda key: res_book[key], lambda key: ctrl_book[key])
        outcome = tfp.decide_verdict(results, accounting)
        run = tfp.FrameProbeRun(outcome=outcome, results=tuple(results),
                                accounting=accounting, population=population)
        if provenance is None:
            provenance = _provenance()
        return run, tfp.render_evidence_payload(run, provenance)

    def test_7_render_is_deterministic_and_byte_identical(self):
        run, payload_a = self._run_and_payload(
            [self.scaled_resident, self.scaled_resident])
        self.assertEqual(payload_a["verdict"], VERDICT_TARGETS_ARE_SCALED)
        payload_b = tfp.render_evidence_payload(run, _provenance())
        self.assertEqual(payload_a, payload_b)
        bytes_a = json.dumps(payload_a, sort_keys=True, indent=2) + "\n"
        bytes_b = json.dumps(payload_b, sort_keys=True, indent=2) + "\n"
        self.assertEqual(bytes_a, bytes_b)

    def test_8_d05_payload_completeness(self):
        _, payload = self._run_and_payload(
            [self.scaled_resident, self.scaled_resident])
        required = {
            "schema_version", "repo_commit", "probe_invocation", "manifests",
            "blacklist_sha256", "data_root_source", "dtype", "device",
            "torch_version", "D_characteristic_length", "T_characteristic_time",
            "arms", "population", "exclusion_counts", "trajectories",
            "aggregates", "tolerance_derivation", "confound_register",
            "verdict", "rationale",
        }
        self.assertLessEqual(required, set(payload))
        self.assertEqual(payload["schema_version"], tfp.PROBE_SCHEMA_VERSION)
        self.assertEqual(len(payload["manifests"]), 1)
        manifest = payload["manifests"][0]
        self.assertEqual(set(manifest), {"label", "path", "sha256"})
        self.assertFalse(Path(manifest["path"]).is_absolute())
        # All four arms with their CoordinateConvention tuples + softening.
        self.assertEqual(
            set(payload["arms"]),
            {ARM_SCALED, ARM_RAW, ARM_POSITIVE_CONTROL, ARM_PROVENANCE_CONTROL})
        for arm_payload in payload["arms"].values():
            self.assertEqual(set(arm_payload["convention"]),
                             {"position", "time", "velocity", "masses"})
            self.assertIn("softening", arm_payload)
        # Per-trajectory rows sorted by key triple, with per-arm medians/maxes,
        # the tolerance triple, booleans, and confound fields.
        rows = payload["trajectories"]
        self.assertEqual(len(rows), 2)
        triples = [(row["key"]["variant"], row["key"]["fidelity"], row["key"]["id"])
                   for row in rows]
        self.assertEqual(triples, sorted(triples))
        for row in rows:
            self.assertEqual(set(row["arms"]), set(payload["arms"]))
            for arm_row in row["arms"].values():
                self.assertIn("median", arm_row)
                self.assertIn("maximum", arm_row)
            for field in ("tolerance_floor", "tolerance_fp32_increment",
                          "numerical_tolerance", "consistency", "separation",
                          "confounds", "membership"):
                self.assertIn(field, row)
        # Aggregate distributions are labeled descriptive, never classification.
        for aggregate in payload["aggregates"].values():
            self.assertEqual(aggregate["role"], "descriptive_diagnostic")
        self.assertIsInstance(payload["tolerance_derivation"], str)
        self.assertIn("max(", payload["tolerance_derivation"])
        # Population accounting: counts, eligible count, exclusion ledger.
        population = payload["population"]
        self.assertEqual(population["eligible_count"], 2)
        self.assertEqual(population["counts_per_split_per_manifest"]["seed42"],
                         {"train": 1, "validation": 1})
        self.assertEqual(population["exclusion_counts"], {"test_under_seed42": 1})
        self.assertEqual(
            population["exclusion_ledger"]["test_under_seed42"],
            [{"variant": "hierarchical", "id": 1002}])
        self.assertIsInstance(payload["confound_register"], list)

    def test_9_redaction_drops_host_absolute_paths(self):
        home = Path.home()
        fake_root = home / "conf01-fake-corpus"
        argv = ["--manifest", "configs/splits.json",
                "--data-root", str(fake_root),
                "--evidence-root", str(home / "conf01-fake-evidence")]
        provenance = _provenance(
            probe_invocation=tfp._reduced_invocation(argv, tfp._REPO_ROOT))
        run, _ = self._run_and_payload([self.scaled_resident, self.scaled_resident])
        payload = tfp.render_evidence_payload(run, provenance)
        raw = json.dumps(payload, sort_keys=True, indent=2) + "\n"
        # No path separator sequence beginning at the filesystem root followed
        # by a user home segment survives serialization.
        self.assertNotIn(str(home), raw)
        self.assertNotIn(str(fake_root), raw)
        # The invocation still records the flags with basename-reduced values.
        invocation = payload["probe_invocation"]
        self.assertIn("--data-root", invocation)
        self.assertIn("conf01-fake-corpus", invocation)
        self.assertIn("conf01-fake-evidence", invocation)

    def test_10_evidence_root_containment_and_non_overwriting_runs(self):
        _, payload = self._run_and_payload(
            [self.scaled_resident, self.scaled_resident])
        # Refusal: an evidence root inside simulation_data.
        with self.assertRaises(ValueError):
            tfp.write_frame_probe_evidence(
                payload, tfp._REPO_ROOT / "simulation_data" / "conf01-evidence")
        # Refusal: an evidence root inside the supplied corpus root.
        corpus = self.tmp / "corpus"
        corpus.mkdir()
        with self.assertRaises(ValueError):
            tfp.write_frame_probe_evidence(
                payload, corpus / "nested", data_root=corpus)
        # Two writes allocate non-overwriting UTC run directories with
        # byte-identical raw.json (deterministic serialization, D-05).
        root = self.tmp / "evidence"
        run_dir_a = tfp.write_frame_probe_evidence(payload, root)
        run_dir_b = tfp.write_frame_probe_evidence(payload, root)
        self.assertNotEqual(run_dir_a, run_dir_b)
        raw_a = (run_dir_a / "raw.json").read_bytes()
        raw_b = (run_dir_b / "raw.json").read_bytes()
        self.assertEqual(raw_a, raw_b)
        summary = (run_dir_a / "summary.md").read_text(encoding="utf-8")
        self.assertIn(VERDICT_TARGETS_ARE_SCALED, summary)
        self.assertIn("**2**", summary)  # population size in the headline

    def test_11_non_finite_measures_serialize_as_sentinels(self):
        nan_resident = (self.traj.times_raw,
                        np.full_like(self.traj.positions_raw, np.nan),
                        np.full_like(self.traj.velocities_raw, np.nan),
                        self.traj.masses)
        _, payload = self._run_and_payload([nan_resident, self.scaled_resident])
        # The 46-02 classifier already routes non-finite measures fail-closed.
        self.assertEqual(payload["verdict"], VERDICT_AMBIGUOUS)
        medians = [arm["median"] for row in payload["trajectories"]
                   for arm in row["arms"].values()]
        self.assertIn("NaN", medians)
        # Strict JSON: no bare non-finite tokens survive serialization.
        raw = json.dumps(payload, sort_keys=True, indent=2, allow_nan=False)
        self.assertIn('"NaN"', raw)

    def test_12_cli_help_names_exactly_the_sanctioned_flags(self):
        completed = subprocess.run(
            [sys.executable, "-m", "pinn.verification.target_frame_probe", "--help"],
            capture_output=True, text=True, cwd=str(tfp._REPO_ROOT))
        self.assertEqual(completed.returncode, 0)
        usage = completed.stdout
        for flag in ("--manifest", "--evidence-root", "--data-root",
                     "--blacklist-path", "--chunk-size"):
            self.assertIn(flag, usage)
        for forbidden in ("--split", "--precision", "--sample"):
            self.assertNotIn(forbidden, usage)


if __name__ == "__main__":
    unittest.main()
