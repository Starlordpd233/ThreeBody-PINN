"""Phase 60 (SPEC Requirements 4 and 5, D-10, GAP-60-08): the real-arm record and its validator.

A real-arm record is the result, so it must be complete: every hash and version SPEC
Requirement 4 names, beside every result field SPEC Requirement 5 names. ``validate_record``
is the gate, ``build_real_record`` is the assembler, and ``run_arm`` writes nothing it has not
validated.

``ValidatorTests`` removes one required field at a time and proves each one is named.
``RealRecordAssemblyTests`` assembles a record without training anything and shows the write
step refuses an invalid one. ``ProbeRecordTests`` reads the two conditional shapes: the probe's
reference in force and S_H, and the continue arm's ruling block. ``WeightsFormatTests`` runs a
fixture arm on MPS float32 and checks the two ``.weights`` files the record describes.

The pattern follows ``tests/phase59/test_evidence_io.py`` (redaction, an atomic write that
returns a SHA-256, and a second launch refused).
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import platform
import re
import subprocess
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import torch

from pinn.verification import learnability_run
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.learnability_arms import (
    FORMULA_NOT_APPLICABLE,
    REAL_RUNTIME,
    RUN_SCHEMA,
    SEED,
    arm_evidence_dir,
    arm_spec,
    fixture_arm,
)
from pinn.verification.learnability_data import fixture_context
from pinn.verification.learnability_run import (
    REQUIRED_REAL_FIELDS,
    R_REF_NOTE,
    build_real_record,
    run_arm,
    validate_record,
)
from tests.phase60._fixtures import gold_corpus_fixture
from tests.phase60.test_scorer_mps import mps_device_or_stop

ROOT = Path(__file__).resolve().parents[2]
HEX64 = re.compile(r"[0-9a-f]{64}")
FIXTURE_RUNTIME = ("float64", "cpu")
PROTOCOL_SHA = "8" * 64
PREFLIGHT_SHA = "9" * 64
SCORECARD_SHA = "7" * 64
SCORER_SHA = "6" * 64
MODULE_PINS = {
    "pinn/verification/learnability_run.py": "5" * 64,
    "pinn/verification/learnability_losses.py": "4" * 64,
}
STATS_SHA = "3" * 64
NORMALIZER_SOURCE = "retained generation-7 checkpoint"
R_REF_VALUE = 19749775821.24417
S_H_VALUE = 22.321729071058996
S_H_EPS = 0.0022321729071058997
S_H_SOURCE = "2" * 64
RULING_SHA = "1" * 64


class _Attestation:
    def __init__(self, *, test_split_opened=0, blocked_attempts=0, refused_before_open=0):
        self._summary = {
            "schema": "phase59-files-opened/v1",
            "data_root_source": "fixture",
            "opened": {"train": 3, "validation": 0, "other_under_root": 0},
            "test_split_opened": test_split_opened,
            "blocked_attempts": blocked_attempts,
            "refused_before_open": refused_before_open,
        }

    def summary(self):
        return dict(self._summary)


def _context(attestation=None):
    return SimpleNamespace(
        attestation=_Attestation() if attestation is None else attestation,
        stats_sha256=STATS_SHA,
        normalizer_source=NORMALIZER_SOURCE,
    )


def _protocol():
    payload = {
        "schema": "phase60-run-protocol/v1",
        "module_sha256": dict(MODULE_PINS),
        "scorecard_sha256": SCORECARD_SHA,
        "scorer_sha256": SCORER_SHA,
    }
    return SimpleNamespace(payload=payload, sha256=PROTOCOL_SHA)


def _admission(spec, *, first_omega_0=30.0, physics=False, s_h=False, ruling=None):
    return {
        "arm_id": spec.arm_id,
        "protocol_sha256": PROTOCOL_SHA,
        "preflight_sha256": PREFLIGHT_SHA,
        "first_omega_0": first_omega_0,
        "omega_provenance": spec.omega_provenance,
        "ruling": ruling,
        "r_ref_in_force": (
            {
                "path": "pinn/verification/artifacts/r_ref_stage0.json",
                "sha256": "c" * 64,
                "value": R_REF_VALUE,
                "note": R_REF_NOTE,
            }
            if physics
            else None
        ),
        "scorer_context_r_ref": (
            {"path": "pinn/verification/artifacts/r_ref_stage0.json", "sha256": "d" * 64}
            if physics
            else None
        ),
        "s_h": (
            {"value": S_H_VALUE, "eps_h": S_H_EPS, "source_sha256": S_H_SOURCE}
            if s_h
            else None
        ),
        "clip_enabled": True,
        "failed_confirmation_pre_answer": None,
    }


def _score(tier=1, E=0.05, eps_h=0.0005, counts=True):
    return {
        "E": E,
        "e_sys_max": E,
        "e_in_max": E / 2.0,
        "h": [[0.01, 0.3], [0.1, 0.8]],
        "eps_h": eps_h,
        "tier": tier,
        "velocity_source": "autograd",
        "grid": "gold",
        "frame": "r_prime_u",
        "n_times": 1001,
        "R_sys": 3.0,
        "physics_residual_mean": 1e-10,
        "physics_residual_max": 2e-10,
    }


def _run_parts(spec, *, first_omega_0=30.0, counted=None, physics=False, probe=False,
               wall_seconds=3600.0):
    """What ``run_arm`` records before the provenance fields are added."""
    counted = spec.counted if counted is None else counted
    counted_flag = True if counted else None
    formula = (
        {
            "E_formula": 0.916813577071981,
            "counts": True,
            "source_sha256": "e" * 64,
        }
        if counted
        else {"E_formula": FORMULA_NOT_APPLICABLE, "counts": None, "source_sha256": None}
    )
    states = {}
    for state in ("adam", "polish"):
        states[state] = {
            "score_gold": _score(),
            "score_base": _score(E=0.06),
            "cross_check": {"tier": 1, "E": 0.05, "eps_h": 0.0005, "counts": counted_flag},
            "weights": {
                "file": f"{state}.weights",
                "sha256": "b" * 64,
                "tensor_digest": "a" * 64,
            },
        }
    parts = {
        "schema": RUN_SCHEMA,
        "diagnostic": True,
        "run_kind": "real",
        "arm_id": spec.arm_id,
        "rung": spec.rung,
        "path": spec.path,
        "loss_arm": spec.loss_arm,
        "system_id": int(spec.system_id),
        "counted": spec.counted,
        "keys": {"train": "hierarchical/gold/1632"},
        "records": {},
        "first_omega_0": first_omega_0,
        "omega_provenance": spec.omega_provenance,
        "grid_omega": spec.grid_omega,
        "seed": SEED,
        "runtime": {"dtype": REAL_RUNTIME[0], "device": REAL_RUNTIME[1]},
        "normalizer": {"stats_sha256": STATS_SHA, "source": NORMALIZER_SOURCE},
        "schedule": {"lr_stage": spec.lr_stage, "cosines": 1},
        "timing": {"steps": 500, "wall_seconds": 3000.0, "seconds_per_step": 6.0},
        "budget": {
            "rule": "frozen",
            "budget_steps": 1800,
            "reading_steps": [0, 90, 1800],
            "readings": [[0, 0.9], [90, 0.4], [1800, 0.05]],
            "outcome": "complete",
            "extended": False,
        },
        "clip": {"stage": spec.clip_stage, "multiplier": 8.5, "enabled": True, "clipped_steps": 3},
        "trace": [{"step": 0, "E": 0.9, "eps_h": 0.1, "tier": 0, "elapsed_seconds": 0.0}],
        "states": states,
        "better_state": "polish",
        "result": {
            "state": "polish",
            "tier": 1,
            "E": 0.05,
            "e_in_max": 0.025,
            "h": [[0.01, 0.3], [0.1, 0.8]],
            "eps_h": 0.0005,
        },
        "formula": formula,
        "wall": {"adam_seconds": 3000.0, "polish_seconds": 100.0,
                 "total_seconds": wall_seconds},
        "attestation": _Attestation().summary(),
        "mps_fallback_env": None,
        "readout_notes": [],
    }
    if physics:
        parts["schedule"]["warmup_steps"] = min(2000, 180)
        parts["monitor_log"] = [
            {
                "step": 0,
                "w_min": 1e-6,
                "w_mean": 0.5,
                "w_max": 0.99,
                "front_idx": 3,
                "residuals_per_bin": [0.1] * 16,
                "raw_residuals_per_bin": [0.1] * 16,
                "r_ref": R_REF_VALUE,
            }
        ]
        parts["handoff"] = {
            "rows_sha256": "f" * 64,
            "w_n": [0.5] * 16,
            "weights": {
                "lambda_data": 1.0,
                "lambda_ic": 1.0,
                "lambda_phys": 1.0,
                "lambda_e": 0.0,
                "lambda_l": 0.0,
            },
        }
    if probe:
        parts["readout_notes"] = [learnability_run._D05_NOTE]
    return parts


def _assemble(spec, **kwargs):
    physics = spec.loss_arm != "data_only"
    first_omega_0 = kwargs.pop("first_omega_0", 30.0)
    admission = _admission(
        spec,
        first_omega_0=first_omega_0,
        physics=physics,
        s_h=spec.rung == "probe-2b",
        ruling=kwargs.pop("ruling", None),
    )
    parts = _run_parts(spec, first_omega_0=first_omega_0, **kwargs)
    return build_real_record(
        spec=spec,
        run_parts=parts,
        admission=admission,
        protocol=_protocol(),
        data_context=_context(),
    )


def _delete(payload, dotted):
    parts = dotted.split(".")
    current = payload
    for part in parts[:-1]:
        current = current[part]
    del current[parts[-1]]


class ValidatorTests(unittest.TestCase):
    """SPEC Requirements 4 and 5: presence, literals and types."""

    def complete(self):
        spec = arm_spec("r1-1632")
        record = _assemble(spec)
        validate_record(record)
        return record

    def test_a_complete_real_record_validates(self):
        record = self.complete()
        for field in REQUIRED_REAL_FIELDS:
            self.assertIn(field.split(".")[0], record, field)

    def test_the_required_field_list_names_both_kinds_of_field(self):
        for field in (
            "protocol_sha256",
            "module_sha256",
            "normalizer.stats_sha256",
            "attestation.test_split_opened",
            "timing.seconds_per_step",
            "wall.hours",
            "budget.readings",
            "states.polish.cross_check",
            "result.e_in_max",
            "formula.counts",
        ):
            self.assertIn(field, REQUIRED_REAL_FIELDS)

    def test_removing_any_required_field_is_refused_and_named(self):
        base = self.complete()
        for field in REQUIRED_REAL_FIELDS:
            with self.subTest(field=field):
                payload = copy.deepcopy(base)
                _delete(payload, field)
                with self.assertRaises(learnability_run.HarnessHalt) as caught:
                    validate_record(payload)
                self.assertIn(field, str(caught.exception))

    def test_a_result_tier_outside_the_ladder_is_refused(self):
        record = self.complete()
        for tier in (4, -1, True, "1"):
            with self.subTest(tier=tier):
                payload = copy.deepcopy(record)
                payload["result"]["tier"] = tier
                with self.assertRaises(learnability_run.HarnessHalt) as caught:
                    validate_record(payload)
                self.assertIn("result.tier", str(caught.exception))

    def test_an_unknown_better_state_is_refused(self):
        payload = copy.deepcopy(self.complete())
        payload["better_state"] = "neither"
        with self.assertRaises(learnability_run.HarnessHalt) as caught:
            validate_record(payload)
        self.assertIn("better_state", str(caught.exception))

    def test_a_horizon_list_without_the_ten_percent_row_is_refused(self):
        payload = copy.deepcopy(self.complete())
        payload["result"]["h"] = [[0.01, 0.3]]
        with self.assertRaises(learnability_run.HarnessHalt) as caught:
            validate_record(payload)
        self.assertIn("0.1", str(caught.exception))

    def test_a_second_seed_is_refused(self):
        payload = copy.deepcopy(self.complete())
        payload["seed"] = 41
        with self.assertRaises(learnability_run.HarnessHalt) as caught:
            validate_record(payload)
        self.assertIn("seed", str(caught.exception))

    def test_a_wrong_runtime_is_refused(self):
        for dtype, device in (("float64", "mps"), ("float32", "cpu")):
            with self.subTest(runtime=(dtype, device)):
                payload = copy.deepcopy(self.complete())
                payload["runtime"] = {"dtype": dtype, "device": device}
                with self.assertRaises(learnability_run.HarnessHalt):
                    validate_record(payload)

    def test_a_fixture_record_is_not_a_real_record(self):
        payload = copy.deepcopy(self.complete())
        payload["run_kind"] = "fixture"
        with self.assertRaises(learnability_run.HarnessHalt) as caught:
            validate_record(payload)
        self.assertIn("run_kind", str(caught.exception))

    def test_a_weights_file_must_be_named_adam_or_polish(self):
        payload = copy.deepcopy(self.complete())
        payload["states"]["adam"]["weights"]["file"] = "adam.pt"
        with self.assertRaises(learnability_run.HarnessHalt) as caught:
            validate_record(payload)
        self.assertIn("states.adam.weights.file", str(caught.exception))

    def test_a_digest_must_be_sixty_four_lowercase_hex_characters(self):
        for bad in ("A" * 64, "a" * 63, "a" * 65, "g" * 64, 7, None):
            with self.subTest(digest=bad):
                payload = copy.deepcopy(self.complete())
                payload["config_sha256"] = bad
                with self.assertRaises(learnability_run.HarnessHalt) as caught:
                    validate_record(payload)
                self.assertIn("config_sha256", str(caught.exception))

    def test_a_nonzero_attestation_counter_is_refused(self):
        for field in ("test_split_opened", "blocked_attempts", "refused_before_open"):
            with self.subTest(field=field):
                payload = copy.deepcopy(self.complete())
                payload["attestation"][field] = 1
                with self.assertRaises(learnability_run.HarnessHalt) as caught:
                    validate_record(payload)
                self.assertIn(field, str(caught.exception))

    def test_a_continue_record_needs_its_ruling_facts(self):
        spec = arm_spec("c-r2b-1632")
        ruling = {
            "path": "evidence/continue/ruling.md",
            "sha256": RULING_SHA,
            "answer": "continue",
            "approved_first_omega_0": 120.0,
            "on_grid": True,
            "equals_confirmed": False,
        }
        record = _assemble(spec, first_omega_0=120.0, physics=True, ruling=ruling)
        validate_record(record)
        self.assertEqual(record["ruling"]["sha256"], RULING_SHA)
        for field in ("sha256", "on_grid", "equals_confirmed"):
            with self.subTest(field=field):
                payload = copy.deepcopy(record)
                del payload["ruling"][field]
                with self.assertRaises(learnability_run.HarnessHalt) as caught:
                    validate_record(payload)
                self.assertIn(field, str(caught.exception))

    def test_a_continue_arm_without_a_ruling_at_all_is_refused(self):
        spec = arm_spec("c-r1u-1632")
        record = _assemble(spec, first_omega_0=120.0, ruling=None)
        with self.assertRaises(learnability_run.HarnessHalt) as caught:
            validate_record(record)
        self.assertIn("ruling", str(caught.exception))

    def test_a_probe_formula_is_null_only_with_the_ratified_note(self):
        spec = arm_spec("p2b-2279")
        record = _assemble(spec, physics=True, probe=True)
        validate_record(record)
        payload = copy.deepcopy(record)
        payload["formula"] = {"E_formula": 0.5, "counts": None, "source_sha256": None}
        with self.assertRaises(learnability_run.HarnessHalt) as caught:
            validate_record(payload)
        self.assertIn("formula.counts", str(caught.exception))

    def test_a_non_finite_number_must_be_the_json_sentinel(self):
        payload = copy.deepcopy(self.complete())
        payload["result"]["eps_h"] = float("nan")
        with self.assertRaises(learnability_run.HarnessHalt):
            validate_record(payload)
        payload["result"]["eps_h"] = "NaN"
        validate_record(payload)


class RealRecordAssemblyTests(unittest.TestCase):
    """SPEC Requirement 4: the assembler fills every provenance field, and nothing invalid is written."""

    def setUp(self):
        self.spec = arm_spec("r1-1632")
        self.record = _assemble(self.spec)

    def test_versions_come_from_the_interpreter_and_the_platform(self):
        self.assertEqual(self.record["versions"]["macos"], platform.mac_ver()[0])
        self.assertEqual(self.record["versions"]["python"], platform.python_version())
        self.assertEqual(self.record["versions"]["torch"], str(torch.__version__))
        self.assertEqual(
            self.record["versions"]["numpy"], str(learnability_run.np.__version__)
        )

    def test_the_code_block_names_the_commit_and_the_dirty_pinn_paths(self):
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=str(ROOT), capture_output=True, text=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(self.record["code"]["git_head"], head)
        self.assertIsInstance(self.record["code"]["dirty_pinn_paths"], list)

    def test_the_config_hash_is_the_canonical_arm_configuration(self):
        expected = learnability_run._config_sha256(
            self.spec,
            first_omega_0=30.0,
            runtime=REAL_RUNTIME,
            budget_steps=self.record["budget"]["budget_steps"],
            clip=self.record["clip"],
        )
        self.assertEqual(self.record["config_sha256"], expected)
        other = learnability_run._config_sha256(
            self.spec,
            first_omega_0=60.0,
            runtime=REAL_RUNTIME,
            budget_steps=self.record["budget"]["budget_steps"],
            clip=self.record["clip"],
        )
        self.assertNotEqual(self.record["config_sha256"], other)

    def test_the_module_pins_and_the_protocol_digest_come_from_the_protocol(self):
        self.assertEqual(self.record["module_sha256"], MODULE_PINS)
        self.assertEqual(self.record["protocol_sha256"], PROTOCOL_SHA)
        self.assertEqual(self.record["scorecard_sha256"], SCORECARD_SHA)
        self.assertEqual(self.record["scorer_sha256"], SCORER_SHA)
        self.assertEqual(self.record["preflight_sha256"], PREFLIGHT_SHA)

    def test_wall_hours_and_seconds_per_step_are_the_measured_values(self):
        self.assertEqual(self.record["wall"]["total_seconds"], 3600.0)
        self.assertEqual(self.record["wall"]["hours"], 1.0)
        self.assertEqual(self.record["timing"]["seconds_per_step"], 6.0)

    def test_the_attestation_and_the_normalizer_digest_are_the_contexts(self):
        self.assertEqual(self.record["attestation"]["test_split_opened"], 0)
        self.assertEqual(self.record["normalizer"]["stats_sha256"], STATS_SHA)
        self.assertEqual(self.record["normalizer"]["source"], NORMALIZER_SOURCE)

    def test_the_assembled_record_is_json_safe(self):
        raw = json.dumps(self.record, allow_nan=False)
        self.assertIn(self.spec.arm_id, raw)

    def test_every_part_of_the_run_is_required(self):
        for field in (
            "budget", "timing", "wall", "states", "result", "formula",
            "first_omega_0", "runtime", "clip",
        ):
            with self.subTest(field=field):
                parts = _run_parts(self.spec)
                del parts[field]
                with self.assertRaises(learnability_run.HarnessHalt) as caught:
                    build_real_record(
                        spec=self.spec,
                        run_parts=parts,
                        admission=_admission(self.spec),
                        protocol=_protocol(),
                        data_context=_context(),
                    )
                self.assertIn(field, str(caught.exception))

    def test_an_admission_for_another_arm_is_refused(self):
        other = _admission(arm_spec("r1-851"))
        with self.assertRaises(learnability_run.HarnessHalt) as caught:
            build_real_record(
                spec=self.spec,
                run_parts=_run_parts(self.spec),
                admission=other,
                protocol=_protocol(),
                data_context=_context(),
            )
        self.assertIn("r1-851", str(caught.exception))

    def test_a_protocol_that_differs_from_the_admission_is_refused(self):
        admission = _admission(self.spec)
        admission["protocol_sha256"] = "0" * 64
        with self.assertRaises(learnability_run.HarnessHalt):
            build_real_record(
                spec=self.spec,
                run_parts=_run_parts(self.spec),
                admission=admission,
                protocol=_protocol(),
                data_context=_context(),
            )

    def test_a_real_record_at_another_runtime_is_refused(self):
        parts = _run_parts(self.spec)
        parts["runtime"] = {"dtype": "float64", "device": "cpu"}
        with self.assertRaises(learnability_run.HarnessHalt) as caught:
            build_real_record(
                spec=self.spec,
                run_parts=parts,
                admission=_admission(self.spec),
                protocol=_protocol(),
                data_context=_context(),
            )
        self.assertIn("float32", str(caught.exception))

    def test_a_missing_attestation_is_refused(self):
        with self.assertRaises(learnability_run.HarnessHalt):
            build_real_record(
                spec=self.spec,
                run_parts=_run_parts(self.spec),
                admission=_admission(self.spec),
                protocol=_protocol(),
                data_context=SimpleNamespace(
                    attestation=None, stats_sha256=STATS_SHA, normalizer_source=NORMALIZER_SOURCE
                ),
            )


class WriteStepTests(unittest.TestCase):
    """SPEC Requirement 4: ``run_arm`` writes no record that ``validate_record`` rejects."""

    def test_an_invalid_record_is_never_written(self):
        with gold_corpus_fixture() as fixture:
            base = fixture_arm(
                train_key=fixture.gold_key,
                score_key=fixture.gold_key,
                beside_key=fixture.base_key,
            )
            spec = dataclasses.replace(base, run_kind="real")
            context = dataclasses.replace(
                fixture_context(
                    allowlist=fixture.allowlist, reader=fixture.reader, stats=fixture.stats
                ),
                run_kind="real",
            )
            admission = {
                "arm_id": spec.arm_id,
                "protocol_sha256": PROTOCOL_SHA,
                "preflight_sha256": PREFLIGHT_SHA,
                "first_omega_0": 30.0,
                "omega_provenance": "locked",
                "ruling": None,
                "r_ref_in_force": None,
                "scorer_context_r_ref": None,
                "s_h": None,
                "clip_enabled": True,
                "failed_confirmation_pre_answer": None,
            }
            with tempfile.TemporaryDirectory(prefix="phase60-write-step-") as root, \
                    mock.patch.object(learnability_run, "REAL_RUNTIME", FIXTURE_RUNTIME), \
                    mock.patch.object(learnability_run, "timing_steps_for", return_value=50), \
                    mock.patch.object(learnability_run, "budget_from_timing", return_value=40), \
                    mock.patch.object(
                        learnability_run, "build_real_record",
                        return_value={"schema": RUN_SCHEMA, "arm_id": spec.arm_id},
                    ):
                with self.assertRaises(learnability_run.HarnessHalt):
                    run_arm(
                        spec,
                        context=context,
                        scorecard=load_scorecard(),
                        runtime=FIXTURE_RUNTIME,
                        evidence_root=Path(root),
                        admission=admission,
                        protocol=_protocol(),
                    )
                arm_dir = arm_evidence_dir(spec.arm_id, evidence_root=Path(root))
                self.assertFalse((arm_dir / "record.json").exists())
                self.assertTrue((arm_dir / "adam.weights").is_file())
                self.assertTrue((arm_dir / "polish.weights").is_file())


class ProbeRecordTests(unittest.TestCase):
    """GAP-60-10, GAP-60-12 and D-05: the probe record's conditional fields."""

    def test_a_probe_rung_two_b_record_names_its_reference_scale_and_note(self):
        spec = arm_spec("p2b-2279")
        record = _assemble(spec, physics=True, probe=True)
        validate_record(record)
        reference = record["r_ref"]
        self.assertEqual(reference["note"], R_REF_NOTE)
        self.assertEqual(reference["value"], R_REF_VALUE)
        self.assertEqual(reference["sha256"], "c" * 64)
        self.assertEqual(reference["path"], "pinn/verification/artifacts/r_ref_stage0.json")
        scale = record["s_h"]
        self.assertEqual(scale["value"], S_H_VALUE)
        self.assertEqual(scale["eps_h"], S_H_EPS)
        self.assertEqual(scale["source_sha256"], S_H_SOURCE)
        self.assertEqual(record["normalizer"]["stats_sha256"], STATS_SHA)
        self.assertTrue(any("D-05" in note for note in record["readout_notes"]))
        # A probe is never counted and never calls counts.
        self.assertEqual(record["formula"]["E_formula"], FORMULA_NOT_APPLICABLE)
        self.assertIsNone(record["formula"]["counts"])

    def test_the_note_is_not_duplicated_when_the_run_already_carried_it(self):
        spec = arm_spec("p2b-2279")
        record = _assemble(spec, physics=True, probe=True)
        self.assertEqual(len(record["readout_notes"]), 1)

    def test_a_continue_physics_arm_records_its_ruling_block(self):
        spec = arm_spec("c-r2b-1632")
        ruling = {
            "path": "evidence/continue/ruling.md",
            "sha256": RULING_SHA,
            "answer": "continue",
            "approved_first_omega_0": 120.0,
            "on_grid": False,
            "equals_confirmed": False,
        }
        record = _assemble(spec, first_omega_0=120.0, physics=True, ruling=ruling)
        validate_record(record)
        self.assertEqual(record["ruling"]["sha256"], RULING_SHA)
        self.assertIs(record["ruling"]["on_grid"], False)
        self.assertIs(record["ruling"]["equals_confirmed"], False)
        self.assertEqual(record["first_omega_0"], 120.0)
        self.assertEqual(record["r_ref"]["note"], R_REF_NOTE)


class WeightsFormatTests(unittest.TestCase):
    """GAP-60-08 and D-10: one ``.weights`` file per scored state, plain git, float32 on MPS."""

    def test_the_two_weights_files_are_the_records_and_nothing_else_is_written(self):
        with gold_corpus_fixture() as fixture:
            device = mps_device_or_stop(self)
            spec = fixture_arm(
                train_key=fixture.gold_key,
                score_key=fixture.gold_key,
                beside_key=fixture.base_key,
            )
            context = fixture_context(
                allowlist=fixture.allowlist, reader=fixture.reader, stats=fixture.stats
            )
            with tempfile.TemporaryDirectory(prefix="phase60-weights-") as root:
                record = run_arm(
                    spec,
                    context=context,
                    scorecard=load_scorecard(),
                    runtime=("float32", device.type),
                    evidence_root=Path(root),
                    fixture_budget_steps=2,
                    fixture_timing_steps=50,
                )
                arm_dir = arm_evidence_dir(spec.arm_id, evidence_root=Path(root))
                self.assertEqual(
                    sorted(path.name for path in arm_dir.iterdir()),
                    ["adam.weights", "polish.weights", "record.json"],
                )
                forbidden = (".pt", ".pth", ".npz", ".npy", ".ckpt", ".pkl")
                for path in arm_dir.iterdir():
                    with self.subTest(name=path.name):
                        self.assertFalse(path.name.endswith(forbidden), path.name)
                for state in ("adam", "polish"):
                    path = arm_dir / f"{state}.weights"
                    recorded = record["states"][state]["weights"]
                    self.assertEqual(
                        hashlib.sha256(path.read_bytes()).hexdigest(), recorded["sha256"]
                    )
                    loaded = torch.load(path, map_location="cpu", weights_only=True)
                    self.assertEqual(
                        learnability_run.weights_digest(loaded), recorded["tensor_digest"]
                    )
                    self.assertTrue(loaded)
                    for tensor in loaded.values():
                        self.assertEqual(tensor.device.type, "cpu")
                        self.assertEqual(tensor.dtype, torch.float32)
                    self.assertRegex(recorded["sha256"], HEX64)
                    self.assertRegex(recorded["tensor_digest"], HEX64)


if __name__ == "__main__":
    unittest.main()
