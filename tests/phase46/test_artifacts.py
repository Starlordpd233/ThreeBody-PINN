"""Dataset-free INST-01 persistence-contract suite (plan 46-05, Task 2).

Pins the D-17/D-18/D-20 artifact contract of
``pinn/training/validation_gate.py``:

- **Atomic publication (D-17):** the durable final sidecar appears at the fixed
  run-relative path, parses, and passes schema validation; no temp-suffix
  residue of the ``atomic_io`` ordering (``path.tmp.{pid}`` -> write -> fsync ->
  os.replace -> dir fsync -> finally-unlink) survives; re-publication is
  byte-identical; a hostile step is rejected before any write.
- **Schema fail-closed (D-18/D-20):** removing EACH required key from an
  otherwise-valid payload makes the validator raise — enumerated over the full
  46-03 schema key list, not a hand-picked subset (T-46-05-04) — plus wrong
  version, unordered rows, row-count disagreement, and non-sentinel string
  metrics.
- **Non-finite retention (D-20):** a NaN per-row ``eps_h`` and an Inf aggregate
  publish successfully as quoted string sentinels under a PLAIN ``json.loads``
  (no custom decoder — any reader can consume them); no gate metric field is
  ever null; the FAIL verdict accompanies the non-finite aggregate.
- **Pointer discipline (D-17/D-20):** the compact ``validation.jsonl`` gate_*
  fields are unobtainable without a durable, schema-valid sidecar — missing,
  truncated, and corrupted sidecars all raise — while a valid-but-FAIL
  observation still yields ``gate_status == "ok"`` pointer fields (a metric
  FAIL is honest evidence, not an instrumentation failure; the two states are
  never conflated).

Dataset-free (D-24): every run directory is a stdlib temp directory; no real
corpus and no production run directory is read.

Frame input rule (same as Task 1's suite): every ``ValidationGateObservation``
constructed here carries an explicit coherent ``FrameConvention`` built INLINE
in this module. The wave-5 production ratified-frame constant does not exist
yet and is never referenced — reaching for it through ``_require`` would
convert this suite into vacuous skips that still exit green (T-46-05-04).

The production module is present (46-03 landed in wave 2), so every test RUNS
— none skip. The ``_require`` helper exists so a wave-misordered checkout
degrades to a localized skip (never an import ERROR), per the tests/phase46
convention.
"""

from __future__ import annotations

import importlib
import json
import math
import tempfile
import unittest
from pathlib import Path

from pinn.verification import gate_metrics

from tests.phase46 import _SKIP_PHRASE
from tests.phase46._fixtures import make_stub_split_sources

_VG_MODULE = "pinn.training.validation_gate"


def _require(symbol, module):
    """Per-symbol deferred import — SkipTest (never ERROR) until it lands."""
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


FrameConvention = _require("FrameConvention", _VG_MODULE)
ValidationGateUnavailable = _require("ValidationGateUnavailable", _VG_MODULE)
TrajectoryGateRow = _require("TrajectoryGateRow", _VG_MODULE)
ValidationGateObservation = _require("ValidationGateObservation", _VG_MODULE)
GATE_SIDECAR_SCHEMA_VERSION = _require("GATE_SIDECAR_SCHEMA_VERSION", _VG_MODULE)
sidecar_relative_path = _require("sidecar_relative_path", _VG_MODULE)
publish_gate_sidecar = _require("publish_gate_sidecar", _VG_MODULE)
validate_sidecar_payload = _require("validate_sidecar_payload", _VG_MODULE)
compact_validation_fields = _require("compact_validation_fields", _VG_MODULE)
compact_validation_fields_from_payload = _require(
    "compact_validation_fields_from_payload", _VG_MODULE
)
POSITION_FRAME_SCALED = _require("POSITION_FRAME_SCALED", _VG_MODULE)
POSITION_FRAME_RAW = _require("POSITION_FRAME_RAW", _VG_MODULE)
TIME_COORD_NORMALIZED = _require("TIME_COORD_NORMALIZED", _VG_MODULE)
TIME_COORD_RAW = _require("TIME_COORD_RAW", _VG_MODULE)
MASS_CONVENTION_ORDERED_RAW = _require("MASS_CONVENTION_ORDERED_RAW", _VG_MODULE)

# The inline coherent frame (D-07 frame-independence): built from the module's
# own constants HERE, never from the wave-5 production constant.
SCALED_FRAME = FrameConvention(
    POSITION_FRAME_SCALED,
    TIME_COORD_NORMALIZED,
    MASS_CONVENTION_ORDERED_RAW,
    conf01_evidence_ref="phase46-05-artifacts-fixture",
)
RAW_FRAME = FrameConvention(
    POSITION_FRAME_RAW,
    TIME_COORD_RAW,
    MASS_CONVENTION_ORDERED_RAW,
    conf01_evidence_ref="phase46-10-artifacts-raw-fixture",
)

# The exact top-level sidecar schema key list recorded in the 46-03 SUMMARY
# ("Sidecar schema keys (D-18 — what 46-07's summary projection and 46-05
# assert)"). The missing-key fail-closed loop enumerates THIS list — the full
# list, never a hand-picked subset (T-46-05-04).
SCHEMA_REQUIRED_KEYS = (
    "schema_version", "run_dir", "sidecar_path", "global_step", "stage",
    "split", "frame", "n_trajectories", "rows", "n_nonfinite",
    "eps_h_reject_threshold", "scs_reject_threshold",
    "aggregate_eps_h", "aggregate_scs", "verdict", "gate_status",
)

# The nested key shape the 46-03 SUMMARY records under ``frame{...}`` and
# ``rows[]{record_key{...}, eps_h, scs}``, pinned on the PUBLISHED payload.
SCHEMA_FRAME_KEYS = ("position_frame", "time_coord", "mass_convention", "conf01_evidence_ref")
SCHEMA_ROW_KEYS = ("record_key", "eps_h", "scs")
SCHEMA_RECORD_KEY_KEYS = ("variant", "fidelity", "id")

# The eight compact ``validation.jsonl`` gate_* keys from the plan's artifact
# table (the 46-03 compact field list the 46-07 wiring emits).
EXPECTED_GATE_FIELDS = (
    "gate_schema_version", "gate_eps_h", "gate_scs", "gate_verdict",
    "gate_status", "gate_n_trajectories", "gate_n_nonfinite", "gate_sidecar",
)

# The three JSON string sentinels ``json_safe_float`` emits (D-20).
SENTINELS = ("NaN", "Infinity", "-Infinity")


# ---------------------------------------------------------------------------
# Observation builder — constructed exactly the way production constructs it
# ---------------------------------------------------------------------------


def _sorted_validation_keys(count):
    """Sorted ``RecordKey``s from the validation member of the disjoint stub pair."""
    _, validation_source = make_stub_split_sources(
        n_train=2, n_validation=count, n_snapshots=8
    )
    keys = sorted(validation_source.records_at_or_below(0))
    if len(keys) != count:
        raise AssertionError("stub validation pool smaller than requested")
    return keys


def make_observation(per_row_eps_h, *, global_step=123, stage=0, frame=None):
    """A ``ValidationGateObservation`` built the way production builds it.

    Per-row SCS is ``gate_metrics.scs_from_eps_h``; the aggregate, verdict, and
    both reject thresholds come from ``gate_metrics`` — no threshold or verdict
    is hand-set anywhere in this suite (D-06/D-13). ``frame`` defaults to the
    module's inline ``SCALED_FRAME``; a caller may pass ``RAW_FRAME`` to build
    the second coherent pair (D-07 frame-independence).
    """
    keys = _sorted_validation_keys(len(per_row_eps_h))
    rows = tuple(
        TrajectoryGateRow(
            record_key=key,
            eps_h=float(eps_h),
            scs=float(gate_metrics.scs_from_eps_h(eps_h)),
        )
        for key, eps_h in zip(keys, per_row_eps_h)
    )
    aggregate = gate_metrics.aggregate_gate_verdict([row.eps_h for row in rows])
    return ValidationGateObservation(
        schema_version=GATE_SIDECAR_SCHEMA_VERSION,
        global_step=int(global_step),
        stage=int(stage),
        split="validation",
        frame=frame if frame is not None else SCALED_FRAME,
        n_trajectories=len(rows),
        rows=rows,
        n_nonfinite=sum(1 for row in rows if not math.isfinite(row.eps_h)),
        eps_h_reject_threshold=float(gate_metrics.GATE_EPS_H_REJECT_THRESHOLD),
        scs_reject_threshold=float(gate_metrics.GATE_SCS_REJECT_THRESHOLD),
        aggregate_eps_h=float(aggregate.eps_h),
        aggregate_scs=float(aggregate.scs),
        verdict=str(aggregate.verdict),
        gate_status="ok",
    )


def _is_legal_metric_json(value):
    """A JSON-decoded metric value is a finite number or one quoted sentinel."""
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    return isinstance(value, str) and value in SENTINELS


class _TempRunDirTestCase(unittest.TestCase):
    """A stdlib-temp run directory per test (D-24: no production run dir)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="phase46-artifacts-")
        self.run_dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def publish(self, observation):
        """Publish and return ``(relative_path, absolute_path)``."""
        rel = publish_gate_sidecar(self.run_dir, observation)
        return rel, self.run_dir / rel

    def published_payload(self, observation):
        """Publish and return the plain-``json.loads`` payload (no custom decoder)."""
        _, path = self.publish(observation)
        return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# D-17 — atomic publication
# ---------------------------------------------------------------------------


class SidecarPublicationTests(_TempRunDirTestCase):
    """D-17: durable final file, no temp residue, idempotent replace, hostile
    step rejected before any write."""

    def test_publish_leaves_valid_final_file_and_no_temp_residue(self):
        observation = make_observation([1e-6, 2e-6, 3e-7])
        rel, path = self.publish(observation)
        self.assertEqual(rel, sidecar_relative_path(observation.global_step))
        self.assertTrue(path.is_file())
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertIs(validate_sidecar_payload(payload), payload)
        # No temp-suffix sibling anywhere under the run dir: the atomic_io
        # ordering (tmp+fsync -> os.replace -> dir fsync -> finally-unlink)
        # leaves nothing behind on success.
        residue = [p for p in self.run_dir.rglob("*") if ".tmp." in p.name]
        self.assertEqual(residue, [])

    def test_republish_is_byte_identical(self):
        observation = make_observation([1e-6, 2e-6, 3e-7])
        _, path = self.publish(observation)
        first = path.read_bytes()
        rel_again, path_again = self.publish(observation)
        self.assertEqual(rel_again, sidecar_relative_path(observation.global_step))
        self.assertEqual(path_again, path)
        self.assertEqual(first, path_again.read_bytes())

    def test_hostile_step_rejected_before_any_write(self):
        for hostile in (-1, True, False):
            with self.subTest(global_step=hostile):
                with self.assertRaises(ValueError):
                    sidecar_relative_path(hostile)
        observation = make_observation([1e-6], global_step=-1)
        with self.assertRaises(ValueError):
            publish_gate_sidecar(self.run_dir, observation)
        self.assertEqual(
            [p for p in self.run_dir.rglob("*")],
            [],
            "a rejected step still wrote something under the run dir",
        )


# ---------------------------------------------------------------------------
# D-18 / D-20 — schema validation fails closed
# ---------------------------------------------------------------------------


class SchemaFailClosedTests(_TempRunDirTestCase):
    """D-18/D-20: a schema-invalid payload is NOT a durable gate record."""

    def setUp(self):
        super().setUp()
        self.payload = self.published_payload(make_observation([1e-6, 2e-6, 3e-7]))

    def test_published_payload_shape_matches_documented_schema(self):
        self.assertEqual(sorted(self.payload.keys()), sorted(SCHEMA_REQUIRED_KEYS))
        self.assertEqual(sorted(self.payload["frame"].keys()), sorted(SCHEMA_FRAME_KEYS))
        for row in self.payload["rows"]:
            self.assertEqual(sorted(row.keys()), sorted(SCHEMA_ROW_KEYS))
            self.assertEqual(
                sorted(row["record_key"].keys()), sorted(SCHEMA_RECORD_KEY_KEYS)
            )

    def test_each_required_key_removed_raises(self):
        # The enumeration source is the full 46-03 SUMMARY schema key list.
        self.assertEqual(len(SCHEMA_REQUIRED_KEYS), 16)
        for key in SCHEMA_REQUIRED_KEYS:
            with self.subTest(missing_key=key):
                broken = dict(self.payload)
                del broken[key]
                with self.assertRaises(ValueError):
                    validate_sidecar_payload(broken)

    def test_wrong_schema_version_raises(self):
        broken = dict(self.payload)
        broken["schema_version"] = "phase46-validation-gate/v0"
        with self.assertRaises(ValueError):
            validate_sidecar_payload(broken)

    def test_rows_out_of_record_key_order_raise(self):
        broken = dict(self.payload)
        broken["rows"] = list(reversed(self.payload["rows"]))
        with self.assertRaises(ValueError):
            validate_sidecar_payload(broken)

    def test_row_count_disagreeing_with_n_trajectories_raises(self):
        for fudge in (+1, -1):
            with self.subTest(fudge=fudge):
                broken = dict(self.payload)
                broken["n_trajectories"] = self.payload["n_trajectories"] + fudge
                with self.assertRaises(ValueError):
                    validate_sidecar_payload(broken)

    def test_unexpected_non_sentinel_string_metric_raises(self):
        for field in ("eps_h", "scs"):
            with self.subTest(row_field=field):
                broken = json.loads(json.dumps(self.payload))  # deep copy
                broken["rows"][0][field] = "not-a-number"
                with self.assertRaises(ValueError):
                    validate_sidecar_payload(broken)
        for field in ("aggregate_eps_h", "aggregate_scs"):
            with self.subTest(aggregate_field=field):
                broken = dict(self.payload)
                broken[field] = "1e-6"  # a numeric STRING is not a legal sentinel
                with self.assertRaises(ValueError):
                    validate_sidecar_payload(broken)

    def test_row_record_key_missing_sub_key_raises(self):
        broken = json.loads(json.dumps(self.payload))  # deep copy
        del broken["rows"][0]["record_key"]["variant"]
        with self.assertRaises(ValueError):
            validate_sidecar_payload(broken)


# ---------------------------------------------------------------------------
# D-20 — non-finite retention as quoted sentinels
# ---------------------------------------------------------------------------


class NonFiniteRetentionTests(_TempRunDirTestCase):
    """D-20: a genuinely non-finite ``eps_H`` is RETAINED as evidence with a
    FAIL verdict — never null-collapsed, never dropped."""

    def _non_finite_observation(self):
        # A NaN per-row eps_h, a +Inf per-row eps_h, and a zero-eps_h row (its
        # derived SCS is -inf — the third sentinel). Built through
        # make_observation exactly like every other fixture in this suite, so
        # the aggregate/SCS/verdict are genuinely DERIVED from gate_metrics
        # over these three rows (D-13) rather than hand-overridden to a value
        # gate_metrics could never itself produce — a strict recomputing
        # validator must be able to re-derive this payload from its own rows.
        return make_observation([float("nan"), float("inf"), 0.0])

    def test_non_finite_metrics_publish_as_quoted_sentinels(self):
        observation = self._non_finite_observation()
        _, path = self.publish(observation)
        raw = path.read_bytes()
        for token in (b'"NaN"', b'"Infinity"', b'"-Infinity"'):
            self.assertIn(token, raw)
        payload = json.loads(raw)  # plain decoder — any reader can consume this
        self.assertEqual(payload["rows"][0]["eps_h"], "NaN")
        self.assertEqual(payload["rows"][0]["scs"], "NaN")
        self.assertEqual(payload["rows"][1]["eps_h"], "Infinity")
        self.assertEqual(payload["rows"][1]["scs"], "NaN")
        self.assertEqual(payload["rows"][2]["eps_h"], 0.0)
        self.assertEqual(payload["rows"][2]["scs"], "-Infinity")
        # aggregate_test_eps_h never returns +Inf: any non-finite per-row
        # value (NaN or Inf alike) poisons the aggregate to NaN (D-13).
        self.assertEqual(payload["aggregate_eps_h"], "NaN")
        self.assertEqual(payload["aggregate_scs"], "NaN")
        # No null appears in ANY gate metric field.
        metric_values = [payload["aggregate_eps_h"], payload["aggregate_scs"]]
        for row in payload["rows"]:
            metric_values.extend([row["eps_h"], row["scs"]])
        for value in metric_values:
            self.assertIsNotNone(value)
            self.assertTrue(
                _is_legal_metric_json(value),
                f"metric field is neither finite nor a quoted sentinel: {value!r}",
            )

    def test_sentinel_payload_is_schema_legal(self):
        observation = self._non_finite_observation()
        payload = self.published_payload(observation)
        self.assertIs(validate_sidecar_payload(payload), payload)

    def test_fail_verdict_accompanies_non_finite_aggregate(self):
        # A real FAIL remains distinguishable from never-computed: the FAIL is
        # persisted in-band with gate_status "ok"; never-computed renders no
        # pointer fields at all (PointerDisciplineTests).
        observation = self._non_finite_observation()
        payload = self.published_payload(observation)
        self.assertEqual(payload["verdict"], "FAIL")
        self.assertEqual(payload["gate_status"], "ok")
        self.assertEqual(payload["n_nonfinite"], 2)


# ---------------------------------------------------------------------------
# D-17 / D-20 — pointer discipline: fields only behind a durable valid sidecar
# ---------------------------------------------------------------------------


class PointerDisciplineTests(_TempRunDirTestCase):
    """D-17/D-20: a JSONL record can never advertise a sidecar that was not
    durably published and schema-validated."""

    def test_missing_sidecar_raises(self):
        observation = make_observation([1e-6, 2e-6])
        with self.assertRaises(ValidationGateUnavailable):
            compact_validation_fields(observation, self.run_dir)

    def test_truncated_sidecar_raises(self):
        observation = make_observation([1e-6, 2e-6])
        _, path = self.publish(observation)
        raw = path.read_bytes()
        path.write_bytes(raw[: len(raw) // 2])
        with self.assertRaises(ValidationGateUnavailable):
            compact_validation_fields(observation, self.run_dir)

    def test_corrupted_required_key_raises(self):
        observation = make_observation([1e-6, 2e-6])
        corruptions = (
            ("verdict-not-pass-fail", lambda p: p.update({"verdict": "INDETERMINATE"})),
            ("dropped-rows", lambda p: p.pop("rows")),
        )
        for name, corrupt in corruptions:
            with self.subTest(corruption=name):
                _, path = self.publish(observation)  # fresh durable sidecar
                payload = json.loads(path.read_text(encoding="utf-8"))
                corrupt(payload)
                path.write_text(
                    json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8"
                )
                with self.assertRaises(ValidationGateUnavailable):
                    compact_validation_fields(observation, self.run_dir)

    def test_valid_sidecar_returns_exactly_eight_gate_keys(self):
        observation = make_observation([1e-6, 2e-6, 3e-7])
        rel, _ = self.publish(observation)
        fields = compact_validation_fields(observation, self.run_dir)
        self.assertEqual(sorted(fields.keys()), sorted(EXPECTED_GATE_FIELDS))
        self.assertEqual(fields["gate_schema_version"], GATE_SIDECAR_SCHEMA_VERSION)
        self.assertEqual(fields["gate_sidecar"], rel)
        self.assertEqual(fields["gate_sidecar"], sidecar_relative_path(observation.global_step))
        self.assertEqual(fields["gate_status"], "ok")
        self.assertEqual(fields["gate_verdict"], "PASS")
        self.assertEqual(fields["gate_n_trajectories"], 3)
        self.assertEqual(fields["gate_n_nonfinite"], 0)
        self.assertEqual(fields["gate_eps_h"], observation.aggregate_eps_h)
        self.assertEqual(fields["gate_scs"], observation.aggregate_scs)

    def test_valid_fail_observation_yields_ok_pointer_fields(self):
        # The instrumentation-failure vs metric-FAIL distinction: a valid
        # observation whose aggregate misses the gate is honest evidence, NOT
        # an instrumentation failure — it still renders gate_status "ok"
        # pointer fields carrying the FAIL verdict.
        observation = make_observation([1.0, 0.5])  # worst case 1.0 misses the gate
        self.assertEqual(observation.verdict, "FAIL")
        rel, _ = self.publish(observation)
        fields = compact_validation_fields(observation, self.run_dir)
        self.assertEqual(sorted(fields.keys()), sorted(EXPECTED_GATE_FIELDS))
        self.assertEqual(fields["gate_status"], "ok")
        self.assertEqual(fields["gate_verdict"], "FAIL")
        self.assertEqual(fields["gate_eps_h"], observation.aggregate_eps_h)
        self.assertEqual(fields["gate_sidecar"], rel)


# ---------------------------------------------------------------------------
# AC-46-10-01 — strict step identity (WR-01 closure)
# ---------------------------------------------------------------------------


class StrictStepIdentityTests(unittest.TestCase):
    """Bool/fraction/string/negative steps cannot alias an integral step's
    sidecar filename; equal and adjacent accepted steps have the expected
    exact identities (AC-46-10-01)."""

    def test_bool_float_string_negative_step_rejected(self):
        for hostile in (True, False, 1.9, "1", "1.0", -1, -0.5):
            with self.subTest(global_step=hostile):
                with self.assertRaises(ValueError):
                    sidecar_relative_path(hostile)

    def test_equal_steps_share_the_identical_identity(self):
        self.assertEqual(sidecar_relative_path(5), sidecar_relative_path(5))
        self.assertEqual(sidecar_relative_path(5), "validation_gate/step-00000005.json")

    def test_adjacent_steps_have_distinct_identities(self):
        self.assertNotEqual(sidecar_relative_path(5), sidecar_relative_path(6))
        self.assertEqual(sidecar_relative_path(6), "validation_gate/step-00000006.json")


# ---------------------------------------------------------------------------
# AC-46-10-02 — every v1 structural/semantic invariant is mutation-tested
# ---------------------------------------------------------------------------


class SemanticInvariantTests(_TempRunDirTestCase):
    """Full v1 semantic contract: frame, split/status, record_key/threshold
    types, and recomputed row/aggregate values all fail closed (AC-46-10-02,
    CR-04)."""

    def setUp(self):
        super().setUp()
        self.payload = self.published_payload(make_observation([1e-6, 2e-6, 3e-7]))

    def test_both_coherent_frame_pairs_are_schema_valid(self):
        scaled_payload = self.published_payload(make_observation([1e-6, 2e-6]))
        self.assertIs(validate_sidecar_payload(scaled_payload), scaled_payload)
        raw_payload = self.published_payload(
            make_observation([1e-6, 2e-6], frame=RAW_FRAME)
        )
        self.assertIs(validate_sidecar_payload(raw_payload), raw_payload)

    def test_frame_key_renamed_to_convention_alias_rejected(self):
        for rename_from, rename_to in (
            ("position_frame", "position_convention"),
            ("time_coord", "time_convention"),
        ):
            with self.subTest(rename=rename_to):
                broken = json.loads(json.dumps(self.payload))
                broken["frame"][rename_to] = broken["frame"].pop(rename_from)
                with self.assertRaises(ValueError):
                    validate_sidecar_payload(broken)

    def test_frame_values_must_be_json_strings(self):
        broken = json.loads(json.dumps(self.payload))
        broken["frame"]["position_frame"] = 123
        with self.assertRaises(ValueError):
            validate_sidecar_payload(broken)

    def test_mass_convention_must_be_ordered_raw(self):
        broken = json.loads(json.dumps(self.payload))
        broken["frame"]["mass_convention"] = "scaled"
        with self.assertRaises(ValueError):
            validate_sidecar_payload(broken)

    def test_empty_conf01_evidence_ref_rejected(self):
        broken = json.loads(json.dumps(self.payload))
        broken["frame"]["conf01_evidence_ref"] = ""
        with self.assertRaises(ValueError):
            validate_sidecar_payload(broken)

    def test_cr04_repro_split_status_step_stage_frame_all_individually_rejected(self):
        # The exact CR-04 reproduction values, each tested individually so a
        # single fixed field cannot mask another's fail-open.
        mutations = (
            ("split", "test"),
            ("gate_status", "failed"),
            ("global_step", -99),
            ("stage", -3),
            ("frame", {}),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                broken = json.loads(json.dumps(self.payload))
                broken[field] = value
                with self.assertRaises(ValueError):
                    validate_sidecar_payload(broken)

    def test_bool_aliases_for_counts_and_ids_rejected(self):
        for field, value in (
            ("n_trajectories", True),
            ("n_nonfinite", False),
            ("global_step", True),
            ("stage", False),
        ):
            with self.subTest(field=field):
                broken = json.loads(json.dumps(self.payload))
                broken[field] = value
                with self.assertRaises(ValueError):
                    validate_sidecar_payload(broken)
        broken = json.loads(json.dumps(self.payload))
        broken["rows"][0]["record_key"]["id"] = True
        with self.assertRaises(ValueError):
            validate_sidecar_payload(broken)

    def test_bool_metrics_and_thresholds_rejected(self):
        for field in ("aggregate_eps_h", "aggregate_scs"):
            with self.subTest(field=field):
                broken = json.loads(json.dumps(self.payload))
                broken[field] = True
                with self.assertRaises(ValueError):
                    validate_sidecar_payload(broken)
        for field in ("eps_h_reject_threshold", "scs_reject_threshold"):
            with self.subTest(field=field):
                broken = json.loads(json.dumps(self.payload))
                broken[field] = True
                with self.assertRaises(ValueError):
                    validate_sidecar_payload(broken)
        broken = json.loads(json.dumps(self.payload))
        broken["rows"][0]["eps_h"] = True
        with self.assertRaises(ValueError):
            validate_sidecar_payload(broken)

    def test_recordkey_variant_and_fidelity_must_be_nonempty_strings(self):
        for field, value in (("variant", ""), ("fidelity", 123)):
            with self.subTest(field=field):
                broken = json.loads(json.dumps(self.payload))
                broken["rows"][0]["record_key"][field] = value
                with self.assertRaises(ValueError):
                    validate_sidecar_payload(broken)

    def test_duplicate_record_key_triples_rejected(self):
        broken = json.loads(json.dumps(self.payload))
        broken["rows"][1]["record_key"] = dict(broken["rows"][0]["record_key"])
        # Keep n_trajectories/n_nonfinite untouched -- only the triple duplicates.
        with self.assertRaises(ValueError):
            validate_sidecar_payload(broken)

    def test_thresholds_must_equal_canonical_values(self):
        for field in ("eps_h_reject_threshold", "scs_reject_threshold"):
            with self.subTest(field=field):
                broken = json.loads(json.dumps(self.payload))
                broken[field] = broken[field] * 2.0 + 1.0
                with self.assertRaises(ValueError):
                    validate_sidecar_payload(broken)

    def test_row_scs_inconsistent_with_recomputed_scs_rejected(self):
        broken = json.loads(json.dumps(self.payload))
        # A finite, legal-looking, but WRONG scs for row 0's eps_h.
        broken["rows"][0]["scs"] = broken["rows"][0]["scs"] + 1.0
        with self.assertRaises(ValueError):
            validate_sidecar_payload(broken)

    def test_aggregate_inconsistent_with_recomputed_aggregate_rejected(self):
        for field in ("aggregate_eps_h", "aggregate_scs"):
            with self.subTest(field=field):
                broken = json.loads(json.dumps(self.payload))
                broken[field] = 0.123456  # a finite, legal, but wrong value
                with self.assertRaises(ValueError):
                    validate_sidecar_payload(broken)

    def test_verdict_inconsistent_with_recomputed_verdict_rejected(self):
        broken = json.loads(json.dumps(self.payload))
        broken["verdict"] = "FAIL" if broken["verdict"] == "PASS" else "PASS"
        with self.assertRaises(ValueError):
            validate_sidecar_payload(broken)


# ---------------------------------------------------------------------------
# AC-46-10-03 — expected run/step/path contextual identity binding
# ---------------------------------------------------------------------------


class IdentityBindingTests(_TempRunDirTestCase):
    """``expected_run_dir_name``/``expected_global_step``/``expected_sidecar_path``
    reject cross-run, wrong-step, and forged-pointer receipts before compact
    fields are returned (AC-46-10-03, CR-03)."""

    def setUp(self):
        super().setUp()
        self.observation = make_observation([1e-6, 2e-6], global_step=7)
        self.rel, _ = self.publish(self.observation)
        self.payload = json.loads((self.run_dir / self.rel).read_text(encoding="utf-8"))

    def _call(self, **overrides):
        kwargs = dict(
            expected_run_dir_name=self.run_dir.name,
            expected_global_step=self.observation.global_step,
            expected_sidecar_path=self.rel,
        )
        kwargs.update(overrides)
        return compact_validation_fields_from_payload(self.payload, **kwargs)

    def test_matching_identity_succeeds(self):
        fields = self._call()
        self.assertEqual(fields["gate_sidecar"], self.rel)

    def test_wrong_step_identity_rejected(self):
        with self.assertRaises(ValueError):
            self._call(expected_global_step=self.observation.global_step + 1)

    def test_cross_run_name_rejected(self):
        with self.assertRaises(ValueError):
            self._call(expected_run_dir_name="a-different-run-name")

    def test_forged_sidecar_path_rejected(self):
        with self.assertRaises(ValueError):
            self._call(expected_sidecar_path="../donor/validation_gate/step-00000007.json")

    def test_path_traversal_pointer_is_never_read_by_compact_validation_fields(self):
        # The public seam never accepts an attacker-supplied path at all: it
        # always derives the candidate from observation.global_step, so a
        # donor sidecar elsewhere is simply never reachable -- reproduced by
        # confirming compact_validation_fields raises when nothing was
        # published for a DIFFERENT observation's own step in this run_dir.
        donor_observation = make_observation([9.0], global_step=999)
        with self.assertRaises(ValidationGateUnavailable):
            compact_validation_fields(donor_observation, self.run_dir)


# ---------------------------------------------------------------------------
# AC-46-10-04 — compact fields are payload-derived, not observation-derived
# ---------------------------------------------------------------------------


class PayloadDerivedCompactFieldsTests(_TempRunDirTestCase):
    """All eight compact fields equal the validated persisted payload even
    when the caller's in-memory observation differs (AC-46-10-04)."""

    def test_compact_fields_reflect_disk_payload_not_a_differing_observation(self):
        published_observation = make_observation([1e-6, 2e-6, 3e-7], global_step=42)
        self.publish(published_observation)
        # A DIFFERENT in-memory observation at the SAME step, with a FAIL
        # verdict and different metrics -- its values must never leak into
        # the compact fields (D-17/D-19).
        divergent_observation = make_observation([9.0], global_step=42)
        self.assertNotEqual(divergent_observation.verdict, published_observation.verdict)
        fields = compact_validation_fields(divergent_observation, self.run_dir)
        self.assertEqual(fields["gate_eps_h"], published_observation.aggregate_eps_h)
        self.assertEqual(fields["gate_verdict"], published_observation.verdict)
        self.assertNotEqual(fields["gate_eps_h"], divergent_observation.aggregate_eps_h)
        self.assertNotEqual(fields["gate_verdict"], divergent_observation.verdict)


if __name__ == "__main__":
    unittest.main()
