"""Plan 67-01: the Phase 67 admission boundary, catalog controls and parity.

A committed registration naming ``variant_registry: "phase67"`` admits through
the existing Phase 65 door with the EXP-02 depth-2 variant; every Phase 65
settings refusal still refuses under the Phase 67 registry; the Phase 67
window endpoints must be finite numbers excluding booleans with the start
exactly zero; the one-hour cap, the typed seed and the exclusive attempt
ownership hold; and every refusal is proven to happen before any data access
or optimizer construction with the Phase 65 no-data no-optimizer spies, in
throwaway fixture repositories. The catalog controls pin the sealed Phase 65
and frozen Phase 66 catalogs unchanged, the Phase 67 registry as a fresh
copy-on-registration with duplicates refused in both directions, null and
empty declarations refused, deterministic catalog and layer order, no harness
import in the catalog module, and the locked raw construction still bitwise
the production network at the same seed.
"""

from __future__ import annotations

import ast
import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

import torch

from tests.phase65.test_fit_short import (
    _fit_registration_fixture,
    _fit_symbols,
    _module,
    _NoDataNoOptimizer,
)
from tests.phase67._fixtures import inline_supervisor, phase67_fixture_registration, phase67_settings

CPU = torch.device("cpu")


class Phase67AdmissionTests(unittest.TestCase):
    """The registry-aware admission: every refusal before any data or optimizer."""

    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.tmp = Path(self.stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase67-admission-")
        ))
        self.fit, self.symbols = _fit_symbols(self)
        self.guard = _module(self, "diagnostic_guard")
        self.nodata = self.stack.enter_context(_NoDataNoOptimizer()(self))

    def _admission(self, root):
        return self.symbols["admission"](
            root / "reg/smoke-registration.json", repo_root=root
        )

    def _refuses(self, name, settings_extra):
        root, _commit = _fit_registration_fixture(
            self.tmp / name, settings_extra=settings_extra
        )
        with self.assertRaises(self.fit.DiagnosticFitRefused):
            self._admission(root)

    def test_a_committed_phase67_registration_admits(self):
        root, _commit = phase67_fixture_registration(self.tmp / "ok")
        _admitted_root, doc = self._admission(root)
        self.assertEqual(doc["settings"]["variant_registry"], "phase67")
        self.assertEqual(doc["settings"]["variant"]["name"], "exp02-d2-w256-o30")

    def test_the_same_variant_without_the_key_or_with_null_refuses(self):
        absent = phase67_settings()
        absent.pop("variant_registry")
        root, _commit = _fit_registration_fixture(
            self.tmp / "absent", settings_extra=absent
        )
        with self.assertRaises(self.fit.DiagnosticFitRefused):
            self._admission(root)
        root, _commit = phase67_fixture_registration(
            self.tmp / "null", variant_registry=None
        )
        with self.assertRaises(self.fit.DiagnosticFitRefused):
            self._admission(root)

    def test_unknown_and_non_string_registry_names_refuse(self):
        for value in ("phase65", "", 7, True, 1.5, ["phase67"]):
            with self.subTest(registry=value):
                self._refuses(
                    f"registry-{value!r}".replace("/", "-"),
                    {"variant_registry": value},
                )

    def test_locked12_under_phase67_admits(self):
        root, _commit = _fit_registration_fixture(
            self.tmp / "locked-under-67", settings_extra={"variant_registry": "phase67"}
        )
        _admitted_root, doc = self._admission(root)
        self.assertEqual(doc["settings"]["variant_registry"], "phase67")
        self.assertEqual(doc["settings"]["variant"]["name"], "locked-12")

    def test_variant_field_drift_refuses(self):
        base = phase67_settings()["variant"]
        drifts = {
            "name": "exp02-d2-w256-o31",
            "time_features": "raw_tau",
            "depth": 12,
            "width": 384,
            "learning_rate": 1e-3,
            "window_length": 9.0,
            "first_omega_0": 1000.0,
            "hidden_omega_0": 2.0,
        }
        for field, value in drifts.items():
            with self.subTest(field=field):
                self._refuses(
                    f"drift-{field}",
                    phase67_settings(variant={**base, field: value}),
                )

    def test_every_phase65_settings_refusal_still_applies(self):
        base = phase67_settings()
        cases = {
            "duplicate_cadence": {"similarity_cadence": [0, 5, 5, 15, 20]},
            "cadence_misses_steps": {"similarity_cadence": [0, 5, 10, 15]},
            "cadence_beyond_steps": {"similarity_cadence": [0, 5, 10, 15, 21]},
            "warmup_ge_steps": {"warmup_steps": 20},
            "unknown_variant": {"variant": {**base["variant"], "name": "no-such"}},
            "variant_field_drift": {"variant": {**base["variant"], "width": 128}},
            "measured_mismatch": {"measured_steps": 17},
            "clipping_enabled": {"optimizer": {**base["optimizer"], "clipping": 8.5}},
            "scheduler_enabled": {
                "optimizer": {**base["optimizer"], "scheduler": "cosine"}
            },
            "missing_reading_rule": {"reading_rule": None},
            "bad_orbit_key": {"orbit_key": "hierarchical/gold"},
        }
        for name, extra in cases.items():
            with self.subTest(case=name):
                self._refuses(name, extra)

    def test_invalid_seed_types_refuse(self):
        for label, value in (
            ("bool", True), ("string", "42"), ("float", 1.5), ("null", None),
        ):
            with self.subTest(seed=value):
                self._refuses(f"seed-{label}", phase67_settings(seed=value))

    def test_phase67_window_endpoints_are_typed_and_exact(self):
        """Both endpoints: finite numbers, booleans excluded, start exactly zero.

        The cases run through the full Phase 67 settings (registry and variant
        included), so the refusal is proven on the Phase 67 door. The Phase 65
        door accepts a boolean or numeric-string ``t_start`` through its float
        coercion; the Phase 67 settings consumer refuses both endpoints of
        any other type before any data access.
        """
        for field, value in (
            ("t_start", False),
            ("t_start", "0"),
            ("t_start", "0.0"),
            ("t_start", None),
            ("t_start", [0.0]),
            ("t_end", True),
            ("t_end", "10"),
            ("t_end", [10.0]),
        ):
            with self.subTest(field=field, value=value):
                window = {"t_start": 0.0, "t_end": 10.0, field: value}
                self._refuses(
                    f"window-{field}-{value!r}".replace("/", "-").replace("'", ""),
                    phase67_settings(physical_window=window),
                )
        for name, window in (
            ("int-endpoints", {"t_start": 0, "t_end": 10}),
            ("float-endpoints", {"t_start": 0.0, "t_end": 10.0}),
        ):
            with self.subTest(window=name):
                root, _commit = _fit_registration_fixture(
                    self.tmp / f"window-ok-{name}",
                    settings_extra=phase67_settings(physical_window=window),
                )
                _admitted_root, doc = self._admission(root)
                self.assertEqual(doc["settings"]["physical_window"], window)

    def test_caps_at_or_above_one_hour_still_refuse(self):
        for cap in (3600, 7200):
            with self.subTest(cap=cap):
                self._refuses(f"cap{cap}", phase67_settings(whole_run_cap_seconds=cap))

    def test_a_pre_existing_attempt_refuses_before_protected_operations(self):
        root, _commit = phase67_fixture_registration(self.tmp / "spent-attempt")
        registration = root / "reg/smoke-registration.json"
        output = root / "evidence/spent/record.json"
        output.parent.mkdir(parents=True)
        (output.parent / "attempt.json").write_bytes(
            b'{"schema": "phase65-fit-attempt/v1", "status": "running"}\n'
        )
        import pinn.verification.diagnostic_data as diagnostic_data

        with mock.patch.object(
            self.fit, "open_diagnostic_context", create=True
        ) as context_spy, mock.patch.object(
            diagnostic_data, "open_diagnostic_context", create=True
        ) as data_spy, mock.patch.object(
            torch.optim.Adam, "step"
        ) as adam_spy:
            code = self.symbols["main"](
                ["run", "--registration", str(registration), "--output", str(output)],
                repo_root=root,
                supervisor=inline_supervisor,
            )
        self.assertEqual(code, 2)
        self.assertFalse(output.exists())
        self.assertEqual(context_spy.call_count, 0)
        self.assertEqual(data_spy.call_count, 0)
        self.assertEqual(adam_spy.call_count, 0)
        # The foreign claim is never touched: a second attempt refuses at the
        # claim and leaves the first claim's status exactly as it found it.
        attempt = json.loads((output.parent / "attempt.json").read_bytes())
        self.assertEqual(attempt["status"], "running")

    def test_a_pre_existing_record_refuses_before_the_worker_runs(self):
        root, _commit = phase67_fixture_registration(self.tmp / "spent-record")
        registration = root / "reg/smoke-registration.json"
        output = root / "evidence/spent2/record.json"
        output.parent.mkdir(parents=True)
        output.write_bytes(b"{}\n")

        def supervisor(*_args, **_kwargs):
            raise AssertionError("the worker ran for a spent directory")

        code = self.symbols["main"](
            ["run", "--registration", str(registration), "--output", str(output)],
            repo_root=root,
            supervisor=supervisor,
        )
        self.assertEqual(code, 2)
        self.assertEqual(output.read_bytes(), b"{}\n")


def _run_non_train_case(stack, root_path):
    """Drive one CLI run whose registration names the withheld test key.

    Only ``open_diagnostic_context`` is routed to the fixture context: the
    orbit spec, the Stage-0 TRAIN-only admission and the reference loader are
    the real seam, so a non-train orbit refuses before any record is opened.
    """
    import pinn.verification.diagnostic_data as diagnostic_data
    import pinn.verification.diagnostic_fit as fit_module
    from pinn.verification import evidence_io
    from tests.phase60._fixtures import gold_corpus_fixture
    from tests.phase65.test_fit_short import _loaded

    fixture = stack.enter_context(gold_corpus_fixture())
    _spec, context, _card, _data = _loaded(fixture)
    orbit_key = evidence_io.record_key_str(fixture.test_key)
    root, _commit = phase67_fixture_registration(root_path, orbit_key=orbit_key)
    registration = root / "reg/smoke-registration.json"
    output = root / "evidence/nontrain/record.json"
    with mock.patch.object(
        fit_module, "open_diagnostic_context", create=True, return_value=context,
    ), mock.patch.object(
        diagnostic_data, "load_reference",
        wraps=diagnostic_data.load_reference,
    ) as reference_spy, mock.patch.object(
        torch.optim.Adam, "step"
    ) as adam_spy:
        code = fit_module.main(
            ["run", "--registration", str(registration), "--output", str(output)],
            repo_root=root,
            supervisor=inline_supervisor,
        )
    return code, output, reference_spy, adam_spy


class Phase67NonTrainBoundaryTests(unittest.TestCase):
    """A non-train orbit refuses at the real Stage-0 seam before any open.

    Unlike the admission tests above, no blanket no-data spies are installed:
    the orbit spec, the Stage-0 TRAIN-only admission and the reference loader
    are the real seam, with the context routed to the synthetic corpus.
    """

    def test_a_non_train_orbit_refuses_before_any_corpus_open(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        tmp = Path(stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase67-nontrain-")
        ))
        code, output, reference_spy, adam_spy = _run_non_train_case(
            stack, tmp / "non-train"
        )
        self.assertEqual(code, 2)
        self.assertFalse(output.exists())
        self.assertEqual(reference_spy.call_count, 0)
        self.assertEqual(adam_spy.call_count, 0)
        attempt = json.loads((output.parent / "attempt.json").read_bytes())
        self.assertEqual(attempt["status"], "incomplete")
        # The withheld test key refuses at the allowlist door, a train-only
        # orbit at the Stage-0 door — both "before any path is built".
        self.assertIn("refused before any path is built", attempt["reason"])


class Phase67CatalogControlTests(unittest.TestCase):
    """The sealed catalogs unchanged, the Phase 67 copy fresh, duplicates and
    empty declarations refused, deterministic order, no harness import."""

    def test_the_sealed_and_phase66_registries_are_unchanged(self):
        from pinn.verification.diagnostic_phase66 import PHASE66_REGISTRY, REGISTRIES
        from pinn.verification.diagnostic_variants import LOCKED_12, REGISTRY

        self.assertEqual(list(REGISTRY), ["locked-12"])
        self.assertIs(REGISTRY["locked-12"], LOCKED_12)
        self.assertEqual(
            list(PHASE66_REGISTRY), ["locked-12", "exp01-d1-w384-o1000"]
        )
        self.assertEqual(list(REGISTRIES), ["phase66"])
        with self.assertRaises(TypeError):
            REGISTRY["extra"] = LOCKED_12

    def test_the_phase67_registry_is_a_fresh_copy_in_registration_order(self):
        from pinn.verification.diagnostic_phase67_catalog import (
            EXP02_D2_VARIANT,
            PHASE67_REGISTRY,
        )
        from pinn.verification.diagnostic_variants import LOCKED_12, REGISTRY

        self.assertIsNot(PHASE67_REGISTRY, REGISTRY)
        # Plans 67-02 and 67-06 extend the registry beyond the tracer
        # declaration with the exact D-03/D-04/D-05 ladders and the fresh
        # orbit-specific 851 encoded registrations; the full order is pinned
        # by tests/phase67/test_catalog.py. This pin keeps proving the same
        # facts for the head and tail of the registration order.
        self.assertEqual(
            list(PHASE67_REGISTRY)[:2], ["locked-12", "exp02-d2-w256-o30"]
        )
        self.assertEqual(list(PHASE67_REGISTRY)[-1], "exp04-exp01-f12-851")
        self.assertIs(PHASE67_REGISTRY["locked-12"], LOCKED_12)
        self.assertIs(PHASE67_REGISTRY["exp02-d2-w256-o30"], EXP02_D2_VARIANT)
        with self.assertRaises(TypeError):
            PHASE67_REGISTRY["extra"] = EXP02_D2_VARIANT

    def test_equal_settings_cannot_acquire_the_same_new_name_twice(self):
        from pinn.verification.diagnostic_phase67_catalog import (
            EXP02_D2_VARIANT,
            PHASE67_REGISTRY,
        )
        from pinn.verification.diagnostic_variants import (
            DiagnosticVariant,
            VariantRefused,
            register_variant,
        )

        with self.assertRaises(VariantRefused) as first:
            register_variant(EXP02_D2_VARIANT, into=PHASE67_REGISTRY)
        self.assertIn("exp02-d2-w256-o30", str(first.exception))
        equal_settings = DiagnosticVariant(**{
            **EXP02_D2_VARIANT.to_json_dict(),
        })
        with self.assertRaises(VariantRefused) as second:
            register_variant(equal_settings, into=PHASE67_REGISTRY)
        self.assertIn("exp02-d2-w256-o30", str(second.exception))
        renamed = DiagnosticVariant(**{
            **EXP02_D2_VARIANT.to_json_dict(), "name": "phase67-fixture-copy"
        })
        extended = register_variant(renamed, into=PHASE67_REGISTRY)
        self.assertEqual(list(extended)[-2:], ["exp04-exp01-f12-851",
                                               "phase67-fixture-copy"])
        self.assertEqual(len(extended), len(PHASE67_REGISTRY) + 1)

    def test_null_and_empty_declarations_refuse(self):
        from pinn.verification.diagnostic_phase67_catalog import EXP02_D2_VARIANT
        from pinn.verification.diagnostic_variants import (
            DiagnosticVariant,
            VariantRefused,
        )

        for name, fields in (
            ("null-features", {"time_features": None}),
            ("empty-features", {"time_features": ""}),
            ("empty-name", {"name": ""}),
        ):
            with self.subTest(declaration=name):
                with self.assertRaises(VariantRefused):
                    DiagnosticVariant(**{
                        **EXP02_D2_VARIANT.to_json_dict(), **fields
                    })

    def test_catalog_and_layer_order_are_deterministic(self):
        from pinn.verification.diagnostic_phase67_catalog import EXP02_D2_VARIANT
        from pinn.verification.diagnostic_phase67_records import registered_layers
        from pinn.verification.diagnostic_variants import build_variant

        self.assertEqual(list(EXP02_D2_VARIANT.to_json_dict()), [
            "name", "time_features", "depth", "width", "learning_rate",
            "window_length", "first_omega_0", "hidden_omega_0",
        ])
        self.assertEqual(registered_layers(1), ["input", "h1"])
        self.assertEqual(registered_layers(2), ["input", "h1", "h2"])
        with self.assertRaises(ValueError):
            registered_layers(0)
        for _ in range(2):
            model = build_variant(
                EXP02_D2_VARIANT, seed=42, dtype=torch.float64, device=CPU
            )
            self.assertEqual(len(model.hidden_layers), 2)
            self.assertEqual(registered_layers(2), ["input", "h1", "h2"])

    def test_the_depth2_declaration_matches_d03(self):
        from pinn.verification.diagnostic_phase67_catalog import EXP02_D2_VARIANT
        from pinn.verification.diagnostic_variants import build_variant

        self.assertEqual(EXP02_D2_VARIANT.name, "exp02-d2-w256-o30")
        self.assertEqual(EXP02_D2_VARIANT.time_features, "raw_tau_ic13")
        self.assertEqual(EXP02_D2_VARIANT.depth, 2)
        self.assertEqual(EXP02_D2_VARIANT.width, 256)
        self.assertEqual(EXP02_D2_VARIANT.first_omega_0, 30.0)
        self.assertEqual(EXP02_D2_VARIANT.hidden_omega_0, 1.0)
        self.assertEqual(EXP02_D2_VARIANT.learning_rate, 1e-4)
        self.assertEqual(EXP02_D2_VARIANT.window_length, 10.0)
        model = build_variant(
            EXP02_D2_VARIANT, seed=42, dtype=torch.float64, device=CPU
        )
        self.assertEqual(model.input_layer.omega_0, 30.0)
        self.assertEqual(len(model.hidden_layers), 2)
        parameters = sum(parameter.numel() for parameter in model.parameters())
        self.assertEqual(parameters, 137737)
        self.assertLess(parameters, 795657)

    def test_the_catalog_imports_no_harness_module(self):
        import pinn.verification.diagnostic_phase67_catalog as catalog

        forbidden = {
            "pinn.verification.diagnostic_fit",
            "pinn.verification.diagnostic_guard",
            "pinn.verification.diagnostic_data",
            "pinn.verification.diagnostic_similarity",
            "pinn.verification.diagnostic_power",
            "pinn.verification.diagnostic_phase66",
            "pinn.verification.diagnostic_phase67_records",
        }
        source = Path(catalog.__file__)
        tree = ast.parse(source.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertNotIn(alias.name, forbidden)
            elif isinstance(node, ast.ImportFrom) and node.module:
                self.assertNotIn(node.module, forbidden)
                for name in forbidden:
                    self.assertFalse(
                        node.module.startswith(f"{name}."),
                        f"the catalog imports harness module {node.module}",
                    )


class LockedRawParityTests(unittest.TestCase):
    """The sealed locked-12 catalog still builds the production network bitwise."""

    def test_locked_raw_construction_is_bitwise_production(self):
        from pinn.architecture_spec import ArchitectureSpec
        from pinn.network import build_network
        from pinn.verification.diagnostic_variants import build_variant

        production = build_network(
            ArchitectureSpec(seed=42), dtype=torch.float64, device=CPU
        )
        variant_net = build_variant(
            "locked-12", seed=42, dtype=torch.float64, device=CPU
        )
        production_state = production.state_dict()
        variant_state = variant_net.state_dict()
        self.assertEqual(sorted(production_state), sorted(variant_state))
        for name in sorted(production_state):
            self.assertTrue(
                torch.equal(production_state[name], variant_state[name]), name
            )
