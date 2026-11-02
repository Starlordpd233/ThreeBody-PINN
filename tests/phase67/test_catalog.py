"""Plan 67-02: the Phase 67 ladder catalog — exact arms, counts and parity.

The Phase 67 registry declares D-03's depth ladder (d2/d4/d6/d8/d12 at the
locked width 256, first omega 30, raw 14D input, rate 1e-4, window [0, 10]),
D-04's rate ladder (lr1e-3/lr3e-4/lr1e-4/lr3e-5/lr1e-5 on the locked depth-12
network) and D-05's six input-design arms (locked-raw/locked-f1/locked-f12 and
exp01-raw/exp01-f1/exp01-f12 at rate 1e-4 on the two required backbones), each
with exact deterministic parameter counts. The encoded arms pin the committed
census row's frequency (N_in/10 cycles per physical time unit, system 1632),
``phase67_registry`` resolves an encoded declaration's frequency only from
that validated committed census row and rejects disagreement with the orbit it
names, and every raw arm still builds the production class bitwise from the
locked spec without touching the global RNG. The sealed Phase 65 catalog and
the frozen Phase 66 declarations stay untouched.
"""

from __future__ import annotations

import ast
import json
import math
import unittest
from pathlib import Path

import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.network import SQRSkipResNetSIREN, build_network
from pinn.verification import diagnostic_variants
from pinn.verification.diagnostic_phase67_catalog import (
    EXP02_D2_VARIANT,
    PHASE67_REGISTRY,
    phase67_registry,
)
from pinn.verification.diagnostic_variants import (
    LOCKED_12,
    REGISTRY,
    VariantRefused,
    build_variant,
    register_variant,
)

CPU = torch.device("cpu")
REPO_ROOT = Path(__file__).resolve().parents[2]
CENSUS_PANELS = (
    REPO_ROOT / ".planning" / "phases" / "59-read-only-baseline-scorecard"
    / "evidence" / "census" / "panels.json"
)

#: The exact registration order of the Phase 67 registry after plan 67-02:
#: the sealed ``locked-12`` entry, then D-03's depth ladder, D-04's rate
#: ladder and D-05's six input arms in the plan's listed arm order.
EXPECTED_REGISTRY_ORDER = [
    "locked-12",
    "exp02-d2-w256-o30",
    "exp02-d4-w256-o30",
    "exp02-d6-w256-o30",
    "exp02-d8-w256-o30",
    "exp02-d12-w256-o30",
    "exp03-d12-w256-lr1e-3",
    "exp03-d12-w256-lr3e-4",
    "exp03-d12-w256-lr1e-4",
    "exp03-d12-w256-lr3e-5",
    "exp03-d12-w256-lr1e-5",
    "exp04-locked-raw",
    "exp04-locked-f1",
    "exp04-locked-f12",
    "exp04-exp01-raw",
    "exp04-exp01-f1",
    "exp04-exp01-f12",
]

#: Deterministic CPU float64 seed-42 parameter counts per registered name
#: (the count is topology-only; the seed never changes it). Depth-associated
#: size changes are recorded per D-03; the encoded fan-in change per D-05.
EXPECTED_PARAMETERS = {
    "exp02-d2-w256-o30": 137737,
    "exp02-d4-w256-o30": 269321,
    "exp02-d6-w256-o30": 400905,
    "exp02-d8-w256-o30": 532489,
    "exp02-d12-w256-o30": 795657,
    "exp03-d12-w256-lr1e-3": 795657,
    "exp03-d12-w256-lr3e-4": 795657,
    "exp03-d12-w256-lr1e-4": 795657,
    "exp03-d12-w256-lr3e-5": 795657,
    "exp03-d12-w256-lr1e-5": 795657,
    "exp04-locked-raw": 795657,
    "exp04-locked-f1": 796169,
    "exp04-locked-f12": 796681,
    "exp04-exp01-raw": 157065,
    "exp04-exp01-f1": 157833,
    "exp04-exp01-f12": 158601,
}

#: The committed Phase 59 census rows (``panels.json`` singles) this catalog
#: pins its encoded frequencies from, verbatim.
CENSUS_N_IN_1632 = 10.471994061054543
CENSUS_N_IN_851 = 18.612048388702


def _state_dicts_equal(first, second):
    if list(first) != list(second):
        return False
    return all(torch.equal(first[key], second[key]) for key in first)


class Phase67LadderCatalogTests(unittest.TestCase):
    """The exact declared ladders, their fields, counts and sealed neighbors."""

    def test_the_phase67_registry_holds_the_exact_declared_ladders_in_order(self):
        self.assertIsNot(PHASE67_REGISTRY, REGISTRY)
        self.assertEqual(list(PHASE67_REGISTRY), EXPECTED_REGISTRY_ORDER)
        self.assertIs(PHASE67_REGISTRY["locked-12"], LOCKED_12)
        self.assertIs(PHASE67_REGISTRY["exp02-d2-w256-o30"], EXP02_D2_VARIANT)
        with self.assertRaises(TypeError):
            PHASE67_REGISTRY["extra"] = EXP02_D2_VARIANT

    def test_the_sealed_and_phase66_registries_are_unchanged(self):
        from pinn.verification.diagnostic_phase66 import PHASE66_REGISTRY, REGISTRIES

        self.assertEqual(list(REGISTRY), ["locked-12"])
        self.assertIs(REGISTRY["locked-12"], LOCKED_12)
        self.assertEqual(
            list(PHASE66_REGISTRY), ["locked-12", "exp01-d1-w384-o1000"]
        )
        self.assertEqual(list(REGISTRIES), ["phase66"])

    def test_every_exp02_depth_arm_declares_d03_exactly(self):
        ladder = [PHASE67_REGISTRY[name] for name in EXPECTED_REGISTRY_ORDER[1:6]]
        self.assertEqual([variant.depth for variant in ladder], [2, 4, 6, 8, 12])
        for variant in ladder:
            self.assertEqual(variant.time_features, "raw_tau_ic13")
            self.assertIsNone(variant.feature_frequency)
            self.assertEqual(variant.width, 256)
            self.assertEqual(variant.first_omega_0, 30.0)
            self.assertEqual(variant.hidden_omega_0, 1.0)
            self.assertEqual(variant.learning_rate, 1e-4)
            self.assertEqual(variant.window_length, 10.0)

    def test_every_exp03_rate_arm_declares_d04_exactly(self):
        rates = [1e-3, 3e-4, 1e-4, 3e-5, 1e-5]
        ladder = [PHASE67_REGISTRY[name] for name in EXPECTED_REGISTRY_ORDER[6:11]]
        self.assertEqual([variant.learning_rate for variant in ladder], rates)
        for variant in ladder:
            self.assertEqual(variant.time_features, "raw_tau_ic13")
            self.assertIsNone(variant.feature_frequency)
            self.assertEqual(variant.depth, 12)
            self.assertEqual(variant.width, 256)
            self.assertEqual(variant.first_omega_0, 30.0)
            self.assertEqual(variant.hidden_omega_0, 1.0)
            self.assertEqual(variant.window_length, 10.0)

    def test_every_exp04_arm_declares_d05_exactly(self):
        arms = {
            name.partition("-")[2]: PHASE67_REGISTRY[name]
            for name in EXPECTED_REGISTRY_ORDER[11:17]
        }
        backbones = {
            "locked": {"depth": 12, "width": 256, "first_omega_0": 30.0},
            "exp01": {"depth": 1, "width": 384, "first_omega_0": 1000.0},
        }
        expected_features = {
            "raw": ("raw_tau_ic13", None),
            "f1": ("tau_ic13_fourier1", CENSUS_N_IN_1632 / T_CHARACTERISTIC_TIME),
            "f12": ("tau_ic13_fourier12", CENSUS_N_IN_1632 / T_CHARACTERISTIC_TIME),
        }
        for arm in ("locked-raw", "locked-f1", "locked-f12",
                    "exp01-raw", "exp01-f1", "exp01-f12"):
            variant = arms[arm]
            backbone, _, design = arm.partition("-")
            self.assertIn(f"exp04-{arm}", EXPECTED_REGISTRY_ORDER)
            self.assertEqual(variant.learning_rate, 1e-4, arm)
            self.assertEqual(variant.window_length, 10.0, arm)
            self.assertEqual(variant.hidden_omega_0, 1.0, arm)
            for field, value in backbones[backbone].items():
                self.assertEqual(getattr(variant, field), value, f"{arm}.{field}")
            features, frequency = expected_features[design]
            self.assertEqual(variant.time_features, features, arm)
            if frequency is None:
                self.assertIsNone(variant.feature_frequency, arm)
            else:
                self.assertEqual(variant.feature_frequency, frequency, arm)

    def test_the_arm_resolver_maps_the_exact_arms_and_refuses_the_rest(self):
        from pinn.verification.diagnostic_phase67_catalog import (
            PHASE67_ARMS,
            phase67_variant,
        )

        self.assertEqual(list(PHASE67_ARMS), ["exp02", "exp03", "exp04"])
        self.assertEqual(list(PHASE67_ARMS["exp02"]), ["d2", "d4", "d6", "d8", "d12"])
        self.assertEqual(
            list(PHASE67_ARMS["exp03"]),
            ["lr1e-3", "lr3e-4", "lr1e-4", "lr3e-5", "lr1e-5"],
        )
        self.assertEqual(
            list(PHASE67_ARMS["exp04"]),
            ["locked-raw", "locked-f1", "locked-f12",
             "exp01-raw", "exp01-f1", "exp01-f12"],
        )
        self.assertIs(phase67_variant("exp02", "d2"), EXP02_D2_VARIANT)
        self.assertEqual(phase67_variant("exp04", "exp01-f12").name,
                         "exp04-exp01-f12")
        for experiment, arm in (("exp05", "d2"), ("exp02", "d3"), (None, "d2")):
            with self.subTest(experiment=experiment, arm=arm):
                with self.assertRaises(VariantRefused):
                    phase67_variant(experiment, arm)

    def test_parameter_counts_are_exact_and_deterministic(self):
        for name, expected in EXPECTED_PARAMETERS.items():
            with self.subTest(variant=name):
                model = build_variant(
                    PHASE67_REGISTRY[name], seed=42, dtype=torch.float64, device=CPU
                )
                parameters = sum(p.numel() for p in model.parameters())
                self.assertEqual(parameters, expected)
                again = build_variant(
                    PHASE67_REGISTRY[name], seed=42, dtype=torch.float64, device=CPU
                )
                self.assertTrue(_state_dicts_equal(
                    model.state_dict(), again.state_dict()
                ))

    def test_duplicates_refuse_and_a_fresh_copy_extends_the_registration_order(self):
        with self.assertRaises(VariantRefused):
            register_variant(
                PHASE67_REGISTRY["exp04-locked-f1"], into=PHASE67_REGISTRY
            )
        renamed = diagnostic_variants.DiagnosticVariant(**{
            **PHASE67_REGISTRY["exp02-d2-w256-o30"].to_json_dict(),
            "name": "phase67-fixture-copy",
        })
        extended = register_variant(renamed, into=PHASE67_REGISTRY)
        self.assertEqual(
            list(extended), [*EXPECTED_REGISTRY_ORDER, "phase67-fixture-copy"]
        )
        self.assertEqual(list(PHASE67_REGISTRY), EXPECTED_REGISTRY_ORDER)

    def test_the_catalog_pins_the_committed_census_rows(self):
        from pinn.verification.diagnostic_phase67_catalog import (
            CENSUS_N_IN_1632 as pinned_1632,
        )
        from pinn.verification.diagnostic_phase67_catalog import (
            CENSUS_N_IN_851 as pinned_851,
        )
        from pinn.verification.diagnostic_phase67_catalog import (
            FEATURE_FREQUENCY_1632,
            FEATURE_FREQUENCY_851,
        )

        doc = json.loads(CENSUS_PANELS.read_bytes().decode("utf-8"))
        self.assertEqual(doc["schema"], "phase59-panels/v1")
        rows = {row["id"]: row["N_in"] for row in doc["singles"]}
        self.assertEqual(pinned_1632, rows[1632])
        self.assertEqual(pinned_851, rows[851])
        self.assertEqual(CENSUS_N_IN_1632, rows[1632])
        self.assertEqual(CENSUS_N_IN_851, rows[851])
        self.assertEqual(FEATURE_FREQUENCY_1632, rows[1632] / T_CHARACTERISTIC_TIME)
        self.assertEqual(FEATURE_FREQUENCY_851, rows[851] / T_CHARACTERISTIC_TIME)

    def test_the_catalog_and_time_features_import_no_harness_module(self):
        forbidden = {
            "pinn.verification.diagnostic_fit",
            "pinn.verification.diagnostic_guard",
            "pinn.verification.diagnostic_data",
            "pinn.verification.diagnostic_similarity",
            "pinn.verification.diagnostic_power",
        }
        source_dir = Path(diagnostic_variants.__file__).parent
        for filename in ("diagnostic_phase67_catalog.py",
                         "diagnostic_time_features.py"):
            tree = ast.parse((source_dir / filename).read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertNotIn(alias.name, forbidden, filename)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    self.assertNotIn(node.module, forbidden, filename)
                    for name in forbidden:
                        self.assertFalse(
                            node.module.startswith(f"{name}."),
                            f"{filename} imports harness module {node.module}",
                        )


class Phase67FrequencyResolutionTests(unittest.TestCase):
    """Encoded frequencies resolve from the committed census row, or refuse."""

    def _encoded_settings(self, *, orbit="hierarchical/gold/1632", name=None):
        variant = PHASE67_REGISTRY[name or "exp04-locked-f1"]
        return {
            "variant_registry": "phase67",
            "orbit_key": orbit,
            "variant": variant.to_json_dict(),
        }

    def test_an_encoded_declaration_admits_its_census_orbit(self):
        registry = phase67_registry(self._encoded_settings())
        self.assertIs(registry, PHASE67_REGISTRY)

    def test_an_encoded_declaration_refuses_a_disagreeing_orbit(self):
        from pinn.verification.diagnostic_phase67_catalog import (
            FEATURE_FREQUENCY_851,
        )

        # System 851's census frequency differs from the pinned 1632 row, so
        # the 1632-pinned declaration must refuse rather than run mis-encoded.
        self.assertNotEqual(
            FEATURE_FREQUENCY_851,
            PHASE67_REGISTRY["exp04-locked-f1"].feature_frequency,
        )
        for orbit in ("hierarchical/gold/851", "hierarchical/gold/4658"):
            with self.subTest(orbit=orbit):
                with self.assertRaises(VariantRefused):
                    phase67_registry(self._encoded_settings(orbit=orbit))

    def test_raw_declarations_do_not_consult_the_census(self):
        settings = {
            "variant_registry": "phase67",
            "orbit_key": "hierarchical/gold/851",
            "variant": PHASE67_REGISTRY["exp02-d2-w256-o30"].to_json_dict(),
        }
        self.assertIs(phase67_registry(settings), PHASE67_REGISTRY)

    def test_settings_without_an_orbit_or_variant_select_without_resolution(self):
        self.assertIs(phase67_registry({"variant_registry": "phase67"}),
                      PHASE67_REGISTRY)
        self.assertIs(phase67_registry("phase67"), PHASE67_REGISTRY)
        # ``None`` keeps the sealed Phase 65 default (every Phase 65
        # registration names no registry); a foreign name refuses.
        self.assertIs(phase67_registry(None), REGISTRY)
        self.assertIs(phase67_registry({"variant_registry": None}), REGISTRY)
        with self.assertRaises(VariantRefused):
            phase67_registry({"variant_registry": "phase68"})

    def test_the_census_reader_validates_committed_metadata(self):
        from pinn.verification.diagnostic_phase67_catalog import census_n_in

        self.assertEqual(census_n_in(1632, panels_path=CENSUS_PANELS),
                         CENSUS_N_IN_1632)
        self.assertEqual(census_n_in(851, panels_path=CENSUS_PANELS),
                         CENSUS_N_IN_851)
        original = json.loads(CENSUS_PANELS.read_bytes().decode("utf-8"))
        import copy
        import tempfile

        for mutate, problem in (
            (lambda doc: doc.pop("singles"), "missing singles"),
            (lambda doc: doc.update(schema="other/v9"), "wrong schema"),
            (
                lambda doc: doc["singles"].append({"id": 700, "N_in": "fast"}),
                "non-numeric N_in",
            ),
            (
                lambda doc: doc["singles"].append({"id": 701, "N_in": float("nan")}),
                "non-finite N_in",
            ),
        ):
            with self.subTest(problem=problem), tempfile.TemporaryDirectory() as tmp:
                broken = copy.deepcopy(original)
                mutate(broken)
                broken_path = Path(tmp) / "panels.json"
                broken_path.write_text(json.dumps(broken))
                with self.assertRaises(VariantRefused):
                    census_n_in(701 if problem.startswith("non") else 1632,
                                panels_path=broken_path)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(VariantRefused):
                census_n_in(1632, panels_path=Path(tmp) / "absent.json")

    def test_malformed_frequency_declarations_refuse(self):
        base = PHASE67_REGISTRY["exp04-locked-f1"].to_json_dict()
        for frequency in (None, 0.0, -1.0, float("inf"), float("nan"), True, "1e0"):
            with self.subTest(frequency=frequency):
                with self.assertRaises(VariantRefused):
                    diagnostic_variants.DiagnosticVariant(**{
                        **base, "feature_frequency": frequency
                    })
        raw = PHASE67_REGISTRY["exp04-locked-raw"].to_json_dict()
        with self.assertRaises(VariantRefused):
            diagnostic_variants.DiagnosticVariant(**{
                **raw, "feature_frequency": CENSUS_N_IN_1632 / 10.0
            })
        with self.assertRaises(VariantRefused):
            diagnostic_variants.DiagnosticVariant(**{
                **base, "time_features": "raw_tau_ic13"
            })

    def test_encoded_json_emits_the_frequency_and_raw_json_keeps_its_keys(self):
        encoded = PHASE67_REGISTRY["exp04-locked-f1"].to_json_dict()
        self.assertEqual(encoded["feature_frequency"],
                         CENSUS_N_IN_1632 / T_CHARACTERISTIC_TIME)
        raw = PHASE67_REGISTRY["exp02-d2-w256-o30"].to_json_dict()
        self.assertEqual(list(raw), [
            "name", "time_features", "depth", "width", "learning_rate",
            "window_length", "first_omega_0", "hidden_omega_0",
        ])
        self.assertEqual(
            list(encoded),
            [*list(raw), "feature_frequency"],
        )


class RawParityAndRNGTests(unittest.TestCase):
    """Raw ladder arms stay bitwise production; construction is RNG-clean."""

    def test_the_raw_locked_arms_build_the_production_class_bitwise(self):
        production = build_network(
            ArchitectureSpec(seed=42), dtype=torch.float64, device=CPU
        )
        for name in ("exp02-d12-w256-o30", "exp03-d12-w256-lr1e-4",
                     "exp04-locked-raw"):
            with self.subTest(variant=name):
                model = build_variant(
                    PHASE67_REGISTRY[name], seed=42, dtype=torch.float64, device=CPU
                )
                self.assertIsInstance(model, SQRSkipResNetSIREN)
                self.assertNotIsInstance(
                    model, __import__(
                        "pinn.verification.diagnostic_time_features",
                        fromlist=["DiagnosticTimeFeatureNetwork"],
                    ).DiagnosticTimeFeatureNetwork
                )
                self.assertTrue(_state_dicts_equal(
                    model.state_dict(), production.state_dict()
                ))

    def test_building_ladder_variants_never_touches_the_global_rng(self):
        torch.manual_seed(20261102)
        before = torch.random.get_rng_state()
        for name in ("exp02-d2-w256-o30", "exp04-locked-f12",
                     "exp04-exp01-f1"):
            build_variant(
                PHASE67_REGISTRY[name], seed=7, dtype=torch.float64, device=CPU
            )
        self.assertTrue(torch.equal(before, torch.random.get_rng_state()))

    def test_the_architecture_spec_stays_locked(self):
        with self.assertRaises(ValueError):
            ArchitectureSpec(hidden_depth=4)
        with self.assertRaises(ValueError):
            ArchitectureSpec(input_dim=16)
        self.assertTrue(math.isfinite(T_CHARACTERISTIC_TIME))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
