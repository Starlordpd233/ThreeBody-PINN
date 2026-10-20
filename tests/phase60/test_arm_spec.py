"""Phase 60 (INST-05 b and e): the closed arm catalog, the override matrix and the omega builder.

Arms come only from a closed catalog of 42 ids and run only in the closed
sequences. A first-layer frequency other than the locked 30 is legal only where
the grid, the arm's loss and the committed D-11 ruling allow it. The expected
tables below are written out by hand, row by row, so they do not repeat the
logic that generates the catalog.

The new symbols are reached through helpers, so a run against code that does not
have them yet fails on the planned behavior instead of at import.
"""

from __future__ import annotations

import dataclasses
import importlib
import math
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import MappingProxyType, SimpleNamespace
from unittest import mock

import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.data.types import RecordKey
from pinn.network import build_network
from pinn.verification import learnability_arms as arms
from pinn.verification import learnability_run
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.learnability_arms import ArmSpec, arm_evidence_dir, fixture_arm
from pinn.verification.learnability_data import fixture_context
from pinn.verification.learnability_run import run_arm
from tests.phase60._fixtures import gold_corpus_fixture

CPU = torch.device("cpu")
FIXTURE_RUNTIME = ("float64", "cpu")


def _symbol(case, name):
    value = getattr(arms, name, None)
    case.assertIsNotNone(value, f"pinn.verification.learnability_arms.{name} is missing")
    return value


def _builder_module(case):
    try:
        return importlib.import_module("pinn.verification.diagnostic_architecture")
    except ImportError as exc:  # the module is created by this plan
        case.fail(f"pinn.verification.diagnostic_architecture is missing: {exc}")


def _ruling(value, answer="continue"):
    """A stand-in for the committed D-11 ruling (Plan 60-06 supplies the loader)."""
    return SimpleNamespace(answer=answer, approved_first_omega_0=value, sha256="0" * 64)


GRID = (60.0, 120.0, 240.0, 480.0)

EXPECTED_IDS = (
    "r1-1632", "r1-851", "r1-4658",
    "g2s-1632-w060", "g2s-1632-w120", "g2s-1632-w240", "g2s-1632-w480",
    "g2s-851-w060", "g2s-851-w120", "g2s-851-w240", "g2s-851-w480",
    "g2c-851-w060", "g2c-851-w120", "g2c-851-w240", "g2c-851-w480",
    "g2c-4658-w060", "g2c-4658-w120", "g2c-4658-w240", "g2c-4658-w480",
    "r2a-1632", "r2a-851", "r2a-4658",
    "r2b-1632", "r2b-851", "r2b-4658",
    "p1-2279", "p1-3418", "p2b-2279", "p2b-3418",
    "c-r1u-1632", "c-r1u-851", "c-r1u-4658",
    "c-r2a-1632", "c-r2a-851", "c-r2a-4658",
    "c-r2b-1632", "c-r2b-851", "c-r2b-4658",
    "c-p1-2279", "c-p1-3418", "c-p2b-2279", "c-p2b-3418",
)

# Where each family reads: (variant, train fidelity, scored fidelity, fidelity beside).
_HIER_DATA = ("hierarchical", "gold", "gold", "base")   # r1, g2s, g2c, c-r1u
_HIER_PHYS = ("hierarchical", "base", "gold", "base")   # r2a, r2b, c-r2a, c-r2b
_STD_DATA = ("standard", "gold", "gold", "base")        # p1, c-p1, p2b-3418, c-p2b-3418
_STD_BASE = ("standard", "base", "gold", "base")        # p2b-2279, c-p2b-2279

# arm id -> (rung, path, loss_arm, record layout, system, lr_stage, clip_stage,
#            omega provenance, grid_omega, counted)
ROWS = {}


def _add(arm_id, rung, path, loss_arm, layout, system, stage, provenance, grid_omega, counted):
    ROWS[arm_id] = (rung, path, loss_arm, layout, system, stage, stage, provenance, grid_omega, counted)


for _system in (1632, 851, 4658):
    _add(f"r1-{_system}", "1", "rung1", "data_only", _HIER_DATA, _system, 0, "locked", None, True)
for _system in (1632, 851):
    for _w, _value in (("060", 60.0), ("120", 120.0), ("240", 240.0), ("480", 480.0)):
        _add(f"g2s-{_system}-w{_w}", "g2-sweep", "g2_sweep", "data_only", _HIER_DATA, _system, 0,
             "g2_sweep_override", _value, True)
for _system in (851, 4658):
    for _w, _value in (("060", 60.0), ("120", 120.0), ("240", 240.0), ("480", 480.0)):
        _add(f"g2c-{_system}-w{_w}", "g2-confirmation", "g2_confirmation", "data_only", _HIER_DATA,
             _system, 0, "confirmation_override", _value, True)
for _system in (1632, 851, 4658):
    _add(f"r2a-{_system}", "2a", "g2_passed", "physics_ic", _HIER_PHYS, _system, 0, "locked", None, True)
for _system in (1632, 851, 4658):
    _add(f"r2b-{_system}", "2b", "g2_passed", "full", _HIER_PHYS, _system, 0, "locked", None, True)
_add("p1-2279", "probe-1", "g2_passed", "data_only", _STD_DATA, 2279, 0, "locked", None, False)
_add("p1-3418", "probe-1", "g2_passed", "data_only", _STD_DATA, 3418, 0, "locked", None, False)
_add("p2b-2279", "probe-2b", "g2_passed", "full", _STD_BASE, 2279, 4, "locked", None, False)
_add("p2b-3418", "probe-2b", "g2_passed", "full", _STD_DATA, 3418, 6, "locked", None, False)
for _system in (1632, 851, 4658):
    _add(f"c-r1u-{_system}", "1", "continue", "data_only", _HIER_DATA, _system, 0, "owner_approved", None, True)
for _system in (1632, 851, 4658):
    _add(f"c-r2a-{_system}", "2a", "continue", "physics_ic", _HIER_PHYS, _system, 0, "owner_approved", None, True)
for _system in (1632, 851, 4658):
    _add(f"c-r2b-{_system}", "2b", "continue", "full", _HIER_PHYS, _system, 0, "owner_approved", None, True)
_add("c-p1-2279", "probe-1", "continue", "data_only", _STD_DATA, 2279, 0, "owner_approved", None, False)
_add("c-p1-3418", "probe-1", "continue", "data_only", _STD_DATA, 3418, 0, "owner_approved", None, False)
_add("c-p2b-2279", "probe-2b", "continue", "full", _STD_BASE, 2279, 4, "owner_approved", None, False)
_add("c-p2b-3418", "probe-2b", "continue", "full", _STD_DATA, 3418, 6, "owner_approved", None, False)

_RUNG2_TAIL = (
    "c-r2b-1632", "c-r2b-851", "c-r2b-4658", "c-r2a-1632", "c-r2a-851", "c-r2a-4658",
)
EXPECTED_SEQUENCES = {
    "rung1": ("r1-1632", "r1-851", "r1-4658"),
    "sweep-1632": ("g2s-1632-w060", "g2s-1632-w120", "g2s-1632-w240", "g2s-1632-w480"),
    "sweep-851": ("g2s-851-w060", "g2s-851-w120", "g2s-851-w240", "g2s-851-w480"),
    "rung2": ("r2b-1632", "r2b-851", "r2b-4658", "r2a-1632", "r2a-851", "r2a-4658"),
    "probes": ("p1-2279", "p1-3418", "p2b-2279", "p2b-3418"),
    "continue-rung2-1632": ("c-r1u-1632",) + _RUNG2_TAIL,
    "continue-rung2-851": ("c-r1u-851",) + _RUNG2_TAIL,
    "continue-rung2-4658": ("c-r1u-4658",) + _RUNG2_TAIL,
    "continue-probes": ("c-p1-2279", "c-p1-3418", "c-p2b-2279", "c-p2b-3418"),
}


class TableTests(unittest.TestCase):
    """The hand-written tables agree with the plan before they are used as the oracle."""

    def test_the_expected_table_has_the_42_planned_rows(self):
        self.assertEqual(len(EXPECTED_IDS), 42)
        self.assertEqual(len(set(EXPECTED_IDS)), 42)
        self.assertEqual(set(ROWS), set(EXPECTED_IDS))


class CatalogTests(unittest.TestCase):
    def test_the_catalog_holds_exactly_the_42_planned_ids_in_order(self):
        catalog = _symbol(self, "catalog")()
        self.assertEqual(tuple(catalog), EXPECTED_IDS)
        self.assertEqual(len(catalog), 42)

    def test_the_catalog_is_read_only_and_each_call_agrees(self):
        catalog = _symbol(self, "catalog")
        first = catalog()
        self.assertIsInstance(first, MappingProxyType)
        with self.assertRaises(TypeError):
            first["r1-0000"] = first["r1-1632"]
        with self.assertRaises(TypeError):
            del first["r1-1632"]
        self.assertEqual(tuple(catalog()), tuple(first))
        self.assertIs(catalog()["r1-1632"], first["r1-1632"])

    def test_every_entry_is_an_armspec_whose_id_is_its_key(self):
        for arm_id, spec in _symbol(self, "catalog")().items():
            with self.subTest(arm_id=arm_id):
                self.assertIsInstance(spec, ArmSpec)
                self.assertEqual(spec.arm_id, arm_id)
                self.assertEqual(spec.run_kind, "real")

    def test_arm_spec_returns_the_catalog_entry(self):
        arm_spec = _symbol(self, "arm_spec")
        catalog = _symbol(self, "catalog")()
        for arm_id in EXPECTED_IDS:
            with self.subTest(arm_id=arm_id):
                self.assertIs(arm_spec(arm_id), catalog[arm_id])

    def test_arm_spec_refuses_every_other_id(self):
        arm_spec = _symbol(self, "arm_spec")
        unknown = _symbol(self, "UnknownArm")
        for bad in (
            "../r1-1632", "r1-9999", "R1-1632", "/abs/r1-1632", "/etc/passwd", "", " r1-1632",
            "r1-1632 ", "r1-1632\n", "r1-1632/../r1-851", "fixture-hierarchical-gold-0",
            "g2s-1632-w090", "g2s-4658-w060", "g2c-1632-w060", "sweep-1632", "arm:r1-1632",
            "c-r1u-2279", "p1-1632", "p2b-851", None, 7, ("r1-1632",), Path("r1-1632"),
        ):
            with self.subTest(arm_id=bad):
                with self.assertRaises(unknown):
                    arm_spec(bad)

    def test_the_grid_settings_in_the_catalog_are_the_scorecards_grid(self):
        scorecard_grid = tuple(load_scorecard().section("gate_g2")["grid"])
        self.assertEqual(scorecard_grid, GRID)
        used = {
            spec.grid_omega
            for spec in _symbol(self, "catalog")().values()
            if spec.grid_omega is not None
        }
        self.assertEqual(used, set(GRID))

    def test_panel_probe_and_exit_constants(self):
        self.assertEqual(_symbol(self, "PANEL_SYSTEMS"), (1632, 851, 4658))
        self.assertEqual(_symbol(self, "PANEL_INNER_LAPS"), {1632: 10.47, 851: 18.61, 4658: 39.35})
        self.assertEqual(_symbol(self, "PROBE_STAGES"), {2279: 4, 3418: 6})
        codes = {
            name: _symbol(self, name)
            for name in ("EXIT_OK", "EXIT_REFUSED", "EXIT_OWNER", "EXIT_SIGHUP", "EXIT_SIGINT", "EXIT_SIGTERM")
        }
        self.assertEqual(
            codes,
            {"EXIT_OK": 0, "EXIT_REFUSED": 2, "EXIT_OWNER": 3, "EXIT_SIGHUP": 129,
             "EXIT_SIGINT": 130, "EXIT_SIGTERM": 143},
        )


class SequenceTests(unittest.TestCase):
    def test_the_sequence_names_are_closed(self):
        sequences = _symbol(self, "SEQUENCES")
        expected = set(EXPECTED_SEQUENCES) | {f"arm:{arm_id}" for arm_id in EXPECTED_IDS}
        self.assertEqual(set(sequences), expected)
        self.assertEqual(len(sequences), 9 + 42)
        self.assertIsInstance(sequences, MappingProxyType)
        with self.assertRaises(TypeError):
            sequences["anything"] = ("r1-1632",)

    def test_each_sequence_holds_exactly_its_planned_arms_in_order(self):
        sequences = _symbol(self, "SEQUENCES")
        for name, arm_ids in EXPECTED_SEQUENCES.items():
            with self.subTest(sequence=name):
                self.assertEqual(sequences[name], arm_ids)

    def test_a_single_arm_sequence_names_that_arm_only(self):
        sequences = _symbol(self, "SEQUENCES")
        for arm_id in EXPECTED_IDS:
            with self.subTest(arm_id=arm_id):
                self.assertEqual(sequences[f"arm:{arm_id}"], (arm_id,))

    def test_every_sequence_arm_is_a_catalog_id_and_none_repeats(self):
        catalog = _symbol(self, "catalog")()
        for name, arm_ids in _symbol(self, "SEQUENCES").items():
            with self.subTest(sequence=name):
                self.assertIsInstance(arm_ids, tuple)
                self.assertTrue(arm_ids)
                self.assertEqual(len(set(arm_ids)), len(arm_ids))
                for arm_id in arm_ids:
                    self.assertIn(arm_id, catalog)

    def test_sweeps_run_in_grid_order_and_rung2_runs_2b_first(self):
        sequences = _symbol(self, "SEQUENCES")
        for system in (1632, 851):
            omegas = [_symbol(self, "arm_spec")(arm_id).grid_omega for arm_id in sequences[f"sweep-{system}"]]
            self.assertEqual(omegas, [60.0, 120.0, 240.0, 480.0])
        self.assertEqual([arm_id[:3] for arm_id in sequences["rung2"]], ["r2b"] * 3 + ["r2a"] * 3)

    def test_no_sequence_name_can_be_built_from_anything_else(self):
        sequences = _symbol(self, "SEQUENCES")
        for bad in ("sweep-4658", "continue-rung2-2279", "rung3", "arm:fixture-hierarchical-gold-0",
                    "arm:r1-9999", "arm:", "", "../rung1", "Rung1"):
            with self.subTest(name=bad):
                self.assertNotIn(bad, sequences)


class RecordKeyTests(unittest.TestCase):
    def test_every_arm_matches_its_planned_row(self):
        catalog = _symbol(self, "catalog")()
        for arm_id, row in ROWS.items():
            rung, path, loss_arm, layout, system, lr_stage, clip_stage, provenance, grid, counted = row
            variant, train, score, beside = layout
            with self.subTest(arm_id=arm_id):
                spec = catalog[arm_id]
                self.assertEqual(
                    (spec.rung, spec.path, spec.loss_arm, spec.system_id, spec.variant),
                    (rung, path, loss_arm, system, variant),
                )
                self.assertEqual(spec.train_key, RecordKey(variant, train, system))
                self.assertEqual(spec.score_key, RecordKey(variant, score, system))
                self.assertEqual(spec.beside_key, RecordKey(variant, beside, system))
                self.assertEqual((spec.lr_stage, spec.clip_stage), (lr_stage, clip_stage))
                self.assertEqual((spec.omega_provenance, spec.grid_omega), (provenance, grid))
                self.assertIs(spec.counted, counted)

    def test_stages_are_zero_except_the_four_stage_probe_arms(self):
        stages = {
            arm_id: (spec.lr_stage, spec.clip_stage)
            for arm_id, spec in _symbol(self, "catalog")().items()
            if (spec.lr_stage, spec.clip_stage) != (0, 0)
        }
        self.assertEqual(
            stages,
            {"p2b-2279": (4, 4), "c-p2b-2279": (4, 4), "p2b-3418": (6, 6), "c-p2b-3418": (6, 6)},
        )

    def test_counted_is_true_for_panel_systems_and_false_for_the_probes(self):
        for arm_id, spec in _symbol(self, "catalog")().items():
            with self.subTest(arm_id=arm_id):
                self.assertIs(spec.counted, spec.system_id in (1632, 851, 4658))
                self.assertIs(spec.counted, spec.system_id not in (2279, 3418))

    def test_only_the_ten_assigned_records_are_ever_named(self):
        assigned = {
            RecordKey("hierarchical", fidelity, system)
            for fidelity in ("base", "gold") for system in (1632, 851, 4658)
        } | {
            RecordKey("standard", fidelity, system)
            for fidelity in ("base", "gold") for system in (2279, 3418)
        }
        self.assertEqual(len(assigned), 10)
        used = set()
        for spec in _symbol(self, "catalog")().values():
            for key in (spec.train_key, spec.score_key, spec.beside_key):
                self.assertIsInstance(key, RecordKey)
                used.add(key)
        self.assertEqual(used, assigned)

    def test_an_arm_holds_record_keys_and_never_a_path(self):
        spec = _symbol(self, "arm_spec")("r1-1632")
        for name in ("train_key", "score_key", "beside_key"):
            for bad in ("hierarchical/gold/1632", Path("hierarchical/gold/1632"), ("hierarchical", "gold", 1632), None):
                with self.subTest(field=name, value=bad):
                    with self.assertRaises(TypeError):
                        dataclasses.replace(spec, **{name: bad})
        with gold_corpus_fixture() as fixture:
            keys = dict(
                train_key=fixture.gold_key, score_key=fixture.gold_key, beside_key=fixture.base_key
            )
            for name in keys:
                for bad in ("hierarchical/gold/0", Path("hierarchical/gold/0")):
                    with self.subTest(fixture_field=name, value=bad):
                        with self.assertRaises(TypeError):
                            fixture_arm(**{**keys, name: bad})

    def test_every_catalog_id_is_a_legal_directory_name(self):
        for arm_id in EXPECTED_IDS:
            with self.subTest(arm_id=arm_id):
                self.assertEqual(
                    arm_evidence_dir(arm_id, evidence_root=Path("root")), Path("root") / "arms" / arm_id
                )


class OverrideTests(unittest.TestCase):
    """INST-05(e): check_override over the catalog, the scorecard grid and the ruling."""

    def setUp(self):
        self.card = load_scorecard()
        self.catalog = _symbol(self, "catalog")()
        self.refused = _symbol(self, "OverrideRefused")
        self.check = _symbol(self, "check_override")
        self.resolve = _symbol(self, "resolve_first_omega_0")

    def passes(self, spec, value, ruling=None):
        self.assertIsNone(self.check(spec, value, scorecard=self.card, ruling=ruling), (spec.arm_id, value))

    def refuses(self, spec, value, ruling=None):
        with self.assertRaises(self.refused, msg=f"{spec.arm_id} at {value!r}"):
            self.check(spec, value, scorecard=self.card, ruling=ruling)

    # -- an arm with a physics term ------------------------------------------------

    def test_a_physics_arm_at_the_locked_value_passes(self):
        for arm_id in ("r2a-1632", "r2b-851", "r2b-4658", "p2b-2279", "p2b-3418"):
            with self.subTest(arm_id=arm_id):
                self.passes(self.catalog[arm_id], 30.0)

    def test_a_physics_arm_at_60_is_refused(self):
        for arm_id in ("r2a-1632", "r2a-851", "r2b-851", "r2b-1632", "p2b-2279", "p2b-3418"):
            with self.subTest(arm_id=arm_id):
                self.refuses(self.catalog[arm_id], 60.0)

    def test_a_physics_arm_never_takes_a_grid_provenance(self):
        for arm_id in ("r2a-1632", "r2b-851", "p2b-2279"):
            for provenance in ("g2_sweep_override", "confirmation_override"):
                for value in GRID:
                    with self.subTest(arm_id=arm_id, provenance=provenance, value=value):
                        spec = dataclasses.replace(
                            self.catalog[arm_id], omega_provenance=provenance, grid_omega=value
                        )
                        self.refuses(spec, value)

    def test_a_physics_arm_passes_only_at_the_exact_ruling_value(self):
        for arm_id in ("c-r2a-1632", "c-r2b-851", "c-p2b-2279", "c-r2b-1632", "c-p2b-3418"):
            spec = self.catalog[arm_id]
            with self.subTest(arm_id=arm_id):
                self.passes(spec, 60.0, _ruling(60.0))
                self.passes(spec, 37.5, _ruling(37.5))
                self.refuses(spec, 60.0, _ruling(90.0))
                self.refuses(spec, 90.0, _ruling(60.0))
                self.refuses(spec, 60.0, _ruling(60.0000001))
                self.refuses(spec, 60.0, None)
                self.refuses(spec, 30.0, None)

    def test_a_ruling_that_does_not_answer_continue_authorizes_nothing(self):
        spec = self.catalog["c-r2b-1632"]
        self.refuses(spec, 60.0, _ruling(60.0, answer="go-to-verdict"))
        self.refuses(spec, 60.0, _ruling(60.0, answer=None))
        self.refuses(spec, 60.0, _ruling(None))
        self.refuses(spec, 60.0, SimpleNamespace(approved_first_omega_0=60.0))
        self.refuses(spec, 60.0, SimpleNamespace(answer="continue"))
        for bad in (0.0, -60.0, math.nan, math.inf, True, "60"):
            with self.subTest(approved=bad):
                self.refuses(spec, 60.0, _ruling(bad))

    # -- a data-only arm on the settings sweep -------------------------------------------

    def test_a_sweep_arm_passes_only_at_its_own_grid_value(self):
        for arm_id, spec in self.catalog.items():
            if not arm_id.startswith(("g2s-", "g2c-")):
                continue
            for value in GRID + (30.0, 90.0):
                with self.subTest(arm_id=arm_id, value=value):
                    if value == spec.grid_omega:
                        self.passes(spec, value)
                    else:
                        self.refuses(spec, value)

    def test_the_named_sweep_examples(self):
        spec = self.catalog["g2s-1632-w060"]
        self.passes(spec, 60.0)
        self.refuses(spec, 90.0)
        self.refuses(spec, 120.0)
        self.refuses(spec, 59.999999)

    def test_a_grid_value_off_the_grid_or_missing_is_refused(self):
        spec = self.catalog["g2s-1632-w060"]
        self.refuses(dataclasses.replace(spec, grid_omega=90.0), 90.0)
        self.refuses(dataclasses.replace(spec, grid_omega=None), 60.0)
        self.refuses(dataclasses.replace(spec, grid_omega=60.0, omega_provenance="confirmation_override",
                                         loss_arm="full"), 60.0)

    def test_the_grid_is_read_from_the_scorecard_not_from_a_literal(self):
        spec = self.catalog["g2s-1632-w060"]
        other = SimpleNamespace(section=lambda name: {"grid": (7.0, 9.0), "locked_value": 30.0})
        with self.assertRaises(self.refused):
            self.check(spec, 60.0, scorecard=other)
        self.assertIsNone(
            self.check(dataclasses.replace(spec, grid_omega=7.0), 7.0, scorecard=other)
        )

    def test_a_scorecard_that_disagrees_with_the_architecture_constant_is_refused(self):
        stand_in = SimpleNamespace(section=lambda name: {"grid": GRID, "locked_value": 31.0})
        with self.assertRaises(self.refused):
            self.check(self.catalog["r1-1632"], 30.0, scorecard=stand_in)
        with self.assertRaises(self.refused):
            self.resolve(self.catalog["r1-1632"], scorecard=stand_in)

    # -- a data-only arm at the locked value ------------------------------------------

    def test_a_locked_arm_passes_only_at_exactly_30(self):
        spec = self.catalog["r1-1632"]
        self.passes(spec, 30.0)
        self.passes(spec, 30)
        for bad in (60.0, 31.0, 30.0000001, 29.9999999, 0.0, -30.0, math.nan, math.inf, -math.inf,
                    True, False, "30", "30.0", None, [30.0]):
            with self.subTest(value=bad):
                self.refuses(spec, bad)

    def test_a_locked_arm_carries_no_grid_value(self):
        self.refuses(dataclasses.replace(self.catalog["r1-1632"], grid_omega=60.0), 30.0)
        self.refuses(dataclasses.replace(self.catalog["r2a-1632"], grid_omega=60.0), 30.0)

    # -- an owner-approved data-only arm (the ruling value need not be on the grid) ----------

    def test_an_owner_approved_data_only_arm_takes_the_ruling_value_on_or_off_the_grid(self):
        for arm_id in ("c-r1u-1632", "c-r1u-851", "c-r1u-4658", "c-p1-2279", "c-p1-3418"):
            spec = self.catalog[arm_id]
            with self.subTest(arm_id=arm_id):
                self.passes(spec, 37.5, _ruling(37.5))
                self.passes(spec, 120.0, _ruling(120.0))
                self.refuses(spec, 30.0, _ruling(60.0))
                self.refuses(spec, 37.5, None)
                self.refuses(spec, 37.5, _ruling(37.5, answer="go-to-verdict"))

    # -- resolve_first_omega_0 ------------------------------------------------------------

    def test_resolve_follows_the_provenance(self):
        card = self.card
        self.assertEqual(self.resolve(self.catalog["r1-1632"], scorecard=card), 30.0)
        self.assertEqual(self.resolve(self.catalog["p2b-3418"], scorecard=card), 30.0)
        for arm_id, spec in self.catalog.items():
            if arm_id.startswith(("g2s-", "g2c-")):
                with self.subTest(arm_id=arm_id):
                    self.assertEqual(self.resolve(spec, scorecard=card), spec.grid_omega)
        self.assertEqual(
            self.resolve(self.catalog["c-r2b-1632"], scorecard=card, ruling=_ruling(37.5)), 37.5
        )
        self.assertEqual(
            self.resolve(self.catalog["c-r1u-851"], scorecard=card, ruling=_ruling(240.0)), 240.0
        )

    def test_resolve_refuses_what_it_cannot_name(self):
        card = self.card
        owner = self.catalog["c-r2b-1632"]
        with self.assertRaises(self.refused):
            self.resolve(owner, scorecard=card)
        with self.assertRaises(self.refused):
            self.resolve(owner, scorecard=card, ruling=_ruling(60.0, answer="go-to-verdict"))
        with self.assertRaises(self.refused):
            self.resolve(owner, scorecard=card, ruling=_ruling(None))
        sweep = dataclasses.replace(self.catalog["g2s-1632-w060"], grid_omega=None)
        with self.assertRaises(self.refused):
            self.resolve(sweep, scorecard=card)

    def test_every_catalog_arm_resolves_and_passes_its_own_check(self):
        for arm_id, spec in self.catalog.items():
            ruling = _ruling(60.0) if spec.omega_provenance == "owner_approved" else None
            with self.subTest(arm_id=arm_id):
                value = self.resolve(spec, scorecard=self.card, ruling=ruling)
                self.passes(spec, value, ruling)


class OverrideBeforeBuildTests(unittest.TestCase):
    """The refusal comes from run_arm before any network is built or any record is read."""

    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.fixture = stack.enter_context(gold_corpus_fixture())
        self.root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="phase60-arms-")))

    def _spec(self, **changes):
        return fixture_arm(
            train_key=self.fixture.gold_key, score_key=self.fixture.gold_key,
            beside_key=self.fixture.base_key, **changes,
        )

    def _run(self, spec, **options):
        return run_arm(
            spec,
            context=fixture_context(
                allowlist=self.fixture.allowlist, reader=self.fixture.reader, stats=self.fixture.stats
            ),
            scorecard=load_scorecard(), runtime=FIXTURE_RUNTIME, evidence_root=self.root,
            fixture_budget_steps=3, **options,
        )

    def _assert_refused_before_building(self, spec, **options):
        refused = _symbol(self, "OverrideRefused")
        with mock.patch.object(learnability_run, "build_arm_network", side_effect=AssertionError("built")) as build, \
                mock.patch.object(learnability_run, "load_arm_data", side_effect=AssertionError("read")) as read:
            with self.assertRaises(refused):
                self._run(spec, **options)
        self.assertEqual((build.call_count, read.call_count), (0, 0))
        self.assertEqual(list(self.root.rglob("*")), [])

    def test_off_grid_and_unruled_settings_are_refused_before_any_build(self):
        cases = (
            self._spec(omega_provenance="g2_sweep_override", grid_omega=90.0),
            self._spec(omega_provenance="confirmation_override", grid_omega=0.0),
            self._spec(omega_provenance="owner_approved"),
            self._spec(loss_arm="physics_ic", omega_provenance="confirmation_override", grid_omega=240.0),
        )
        for index, spec in enumerate(cases):
            with self.subTest(case=index):
                self._assert_refused_before_building(spec)

    def test_a_ruling_that_does_not_answer_continue_is_refused_before_any_build(self):
        spec = self._spec(omega_provenance="owner_approved")
        for ruling in (_ruling(60.0, answer="go-to-verdict"), _ruling(None), _ruling(-1.0)):
            with self.subTest(ruling=ruling):
                self._assert_refused_before_building(spec, ruling=ruling)

    def test_an_off_grid_owner_approved_value_runs_end_to_end(self):
        spec = self._spec(omega_provenance="owner_approved")
        record = self._run(spec, ruling=_ruling(37.5))
        self.assertEqual(record["first_omega_0"], 37.5)
        self.assertEqual(record["omega_provenance"], "owner_approved")
        self.assertIsNone(record["grid_omega"])
        arm_dir = arm_evidence_dir(spec.arm_id, evidence_root=self.root)
        self.assertEqual(
            sorted(path.name for path in arm_dir.iterdir()),
            ["adam.weights", "polish.weights", "record.json"],
        )


class BuilderTests(unittest.TestCase):
    """The omega builder: bitwise identity at 30, first-layer frequency only elsewhere."""

    def setUp(self):
        self.builder = _builder_module(self).build_network_with_first_omega
        self.error = _builder_module(self).DiagnosticOmegaError
        self.reference = build_network(ArchitectureSpec(seed=42), dtype=torch.float64, device=CPU)

    def _inputs(self):
        generator = torch.Generator().manual_seed(5)
        points = torch.rand(7, 14, generator=generator, dtype=torch.float64) * 2.0 - 1.0
        masses = torch.rand(7, 3, generator=generator, dtype=torch.float64) + 0.5
        return points, masses

    def test_at_30_every_parameter_is_bitwise_equal_to_build_network(self):
        model = self.builder(30.0, seed=42, dtype=torch.float64, device=CPU)
        expected = self.reference.state_dict()
        actual = model.state_dict()
        self.assertEqual(list(actual), list(expected))
        for name in expected:
            with self.subTest(parameter=name):
                self.assertTrue(torch.equal(actual[name], expected[name]))
        self.assertEqual(model.first_omega_0, 30.0)
        self.assertEqual(model.input_layer.omega_0, 30.0)
        points, masses = self._inputs()
        self.assertTrue(torch.equal(model(points, masses), self.reference(points, masses)))

    def test_at_60_only_the_first_layer_frequency_and_the_forward_differ(self):
        model = self.builder(60.0, seed=42, dtype=torch.float64, device=CPU)
        expected = self.reference.state_dict()
        actual = model.state_dict()
        self.assertEqual(list(actual), list(expected))
        for name in expected:
            with self.subTest(parameter=name):
                self.assertTrue(torch.equal(actual[name], expected[name]))
        self.assertEqual(model.input_layer.omega_0, 60.0)
        self.assertEqual(model.first_omega_0, 60.0)
        self.assertEqual(model.hidden_omega_0, self.reference.hidden_omega_0)
        self.assertEqual(self.reference.input_layer.omega_0, 30.0)
        points, masses = self._inputs()
        self.assertFalse(torch.equal(model(points, masses), self.reference(points, masses)))

    def test_any_positive_frequency_is_built_the_same_way(self):
        for omega in (37.5, 120.0, 480.0, 1e-3):
            with self.subTest(omega=omega):
                model = self.builder(omega, seed=42, dtype=torch.float64, device=CPU)
                self.assertEqual(model.input_layer.omega_0, omega)
                for name, tensor in self.reference.state_dict().items():
                    self.assertTrue(torch.equal(model.state_dict()[name], tensor), name)

    def test_the_seed_still_selects_the_initialization(self):
        a = self.builder(60.0, seed=42, dtype=torch.float64, device=CPU)
        b = self.builder(60.0, seed=7, dtype=torch.float64, device=CPU)
        names = list(a.state_dict())
        self.assertFalse(all(torch.equal(a.state_dict()[n], b.state_dict()[n]) for n in names))
        c = build_network(ArchitectureSpec(seed=7), dtype=torch.float64, device=CPU)
        self.assertTrue(all(torch.equal(b.state_dict()[n], c.state_dict()[n]) for n in names))

    def test_building_does_not_touch_the_global_random_state(self):
        saved = torch.get_rng_state()
        self.addCleanup(torch.set_rng_state, saved)
        torch.manual_seed(12345)  # a state that is not the seed-42 state a careless builder would set
        before = torch.get_rng_state()
        self.builder(60.0, seed=42, dtype=torch.float64, device=CPU)
        self.assertTrue(torch.equal(torch.get_rng_state(), before))

    def test_a_float32_network_is_built_in_float32(self):
        model = self.builder(60.0, seed=42, dtype=torch.float32, device=CPU)
        self.assertTrue(all(p.dtype == torch.float32 for p in model.parameters()))

    def test_a_frequency_that_is_not_a_finite_positive_real_raises(self):
        for bad in (math.nan, math.inf, -math.inf, 0.0, -30.0, -1e-9, True, False, "60", None, [60.0]):
            with self.subTest(value=bad):
                with self.assertRaises(self.error):
                    self.builder(bad, seed=42, dtype=torch.float64, device=CPU)

    def test_the_production_modules_still_refuse_another_frequency(self):
        with self.assertRaises(ValueError):
            ArchitectureSpec(first_omega_0=60.0)
        duck = SimpleNamespace(seed=42, first_omega_0=60.0)
        with self.assertRaises(TypeError):
            build_network(duck, dtype=torch.float64, device=CPU)


if __name__ == "__main__":
    unittest.main()
