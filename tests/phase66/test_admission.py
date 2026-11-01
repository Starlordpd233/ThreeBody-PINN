"""Plan 66-01 (EXP-01): the registry-aware settings admission contract.

A committed registration naming ``variant_registry: "phase66"`` admits through
the existing Phase 65 door with the EXP-01 variant; the same variant without
the key, with a null value, or under an unknown or non-string registry name
refuses; every Phase 65 settings refusal still refuses with the EXP-01 variant
and the phase 66 registry; the one-hour cap, the bounded smoke policy and the
MPS gate hold; and the loss-trace stride admits only absent, null or an
integer from 1 to optimizer_steps. Every refusal is proven to happen before
any data access or optimizer construction with the Phase 65 no-data
no-optimizer spies, in throwaway fixture repositories.
"""

from __future__ import annotations

import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

from tests.phase65.test_fit_short import (
    _fit_registration_fixture,
    _fit_symbols,
    _module,
    _NoDataNoOptimizer,
)
from tests.phase66.test_tracer import phase66_fixture_registration, phase66_settings


class Phase66AdmissionTests(unittest.TestCase):
    """The registry-aware admission: every refusal before any data or optimizer."""

    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.tmp = Path(self.stack.enter_context(
            tempfile.TemporaryDirectory(prefix="phase66-admission-")
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

    def test_a_committed_phase66_registration_admits(self):
        root, _commit = phase66_fixture_registration(self.tmp / "ok")
        _admitted_root, doc = self._admission(root)
        self.assertEqual(doc["settings"]["variant_registry"], "phase66")
        self.assertEqual(doc["settings"]["variant"]["name"], "exp01-d1-w384-o1000")

    def test_the_same_variant_without_the_key_or_with_null_refuses(self):
        absent = phase66_settings()
        absent.pop("variant_registry")
        root, _commit = _fit_registration_fixture(
            self.tmp / "absent", settings_extra=absent
        )
        with self.assertRaises(self.fit.DiagnosticFitRefused):
            self._admission(root)
        root, _commit = phase66_fixture_registration(
            self.tmp / "null", variant_registry=None
        )
        with self.assertRaises(self.fit.DiagnosticFitRefused):
            self._admission(root)

    def test_unknown_and_non_string_registry_names_refuse(self):
        for value in ("phase65", "", 7, True, ["phase66"]):
            with self.subTest(registry=value):
                self._refuses(
                    f"registry-{value!r}".replace("/", "-"),
                    {"variant_registry": value},
                )

    def test_locked12_under_phase66_admits(self):
        root, _commit = _fit_registration_fixture(
            self.tmp / "locked-under-66", settings_extra={"variant_registry": "phase66"}
        )
        _admitted_root, doc = self._admission(root)
        self.assertEqual(doc["settings"]["variant_registry"], "phase66")
        self.assertEqual(doc["settings"]["variant"]["name"], "locked-12")

    def test_variant_field_drift_refuses(self):
        base = phase66_settings()["variant"]
        drifts = {
            "name": "exp01-d1-w384-o999",
            "time_features": "raw_tau",
            "depth": 2,
            "width": 256,
            "learning_rate": 1e-3,
            "window_length": 9.0,
            "first_omega_0": 30.0,
            "hidden_omega_0": 2.0,
        }
        for field, value in drifts.items():
            with self.subTest(field=field):
                self._refuses(
                    f"drift-{field}", {"variant": {**base, field: value}}
                )

    def test_every_phase65_settings_refusal_still_applies(self):
        base = phase66_settings()
        cases = {
            "duplicate_cadence": {"similarity_cadence": [0, 5, 5, 15, 20]},
            "cadence_misses_steps": {"similarity_cadence": [0, 5, 10, 15]},
            "cadence_beyond_steps": {"similarity_cadence": [0, 5, 10, 15, 21]},
            "warmup_ge_steps": {"warmup_steps": 20},
            "unknown_variant": {"variant": {**base["variant"], "name": "no-such"}},
            "variant_field_drift": {"variant": {**base["variant"], "width": 128}},
            "window_drift": {"physical_window": {"t_start": 0.0, "t_end": 9.0}},
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

    def test_caps_at_or_above_one_hour_still_refuse(self):
        for cap in (3600, 7200):
            with self.subTest(cap=cap):
                self._refuses(f"cap{cap}", {"whole_run_cap_seconds": cap})

    def test_a_cap_below_the_hour_boundary_passes_the_cap_gate(self):
        root, _commit = phase66_fixture_registration(
            self.tmp / "cap-ok", whole_run_cap_seconds=3599.5
        )
        _admitted_root, doc = self._admission(root)
        self.assertEqual(doc["settings"]["whole_run_cap_seconds"], 3599.5)

    def test_scheduler_clipping_physics_term_and_polish_still_refuse(self):
        base = phase66_settings()
        for key, value in (
            ("scheduler", "cosine"),
            ("clipping", 8.5),
            ("physics_term", 1.0),
            ("polish", "lbfgs"),
        ):
            with self.subTest(key=key):
                self._refuses(
                    f"policy-{key}",
                    {"optimizer": {**base["optimizer"], key: value}},
                )

    def test_an_mps_registration_without_mps_refuses_before_any_access(self):
        root, _commit = phase66_fixture_registration(
            self.tmp / "mps", runtime={"dtype": "float32", "device": "mps"}
        )
        with mock.patch("torch.backends.mps.is_available", return_value=False):
            with self.assertRaises(self.fit.DiagnosticFitRefused):
                self._admission(root)

    def test_the_loss_trace_stride_matrix(self):
        absent = phase66_settings()  # no loss_trace_stride key at all
        for value in (absent, None, 1, 20):
            with self.subTest(stride="absent" if isinstance(value, dict) else value):
                name = "stride-absent" if isinstance(value, dict) else f"stride-{value}"
                settings_extra = value if isinstance(value, dict) else {
                    "loss_trace_stride": value
                }
                root, _commit = _fit_registration_fixture(
                    self.tmp / name, settings_extra=settings_extra
                )
                _admitted_root, doc = self._admission(root)
                self.assertEqual(
                    doc["settings"].get("loss_trace_stride"),
                    None if isinstance(value, dict) else value,
                )
        for label, value in (
            ("bool", True),
            ("zero", 0),
            ("negative", -1),
            ("float", 1.5),
            ("string", "3"),
            ("over_long", 21),
        ):
            with self.subTest(stride=value):
                self._refuses(f"stride-bad-{label}", {"loss_trace_stride": value})
