"""Phase 41 / Plan 05 — resume identity digest + fail-safe field-classified diff.

CTRL-05: multi-module identity payload, named refuse, exact-anchor load routing,
--hold-stage non-final guard, identity coverage check.
"""

from __future__ import annotations

import importlib
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tests.phase41 import _SKIP_PHRASE

MODULE = "pinn.training.resume"
CONFIG_MODULE = "pinn.training.config"


def _require(symbol, module=MODULE):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


def _make_config(**run_overrides):
    from pinn.training.config import (
        GuardConfig,
        LossConfig,
        OptConfig,
        RunConfig,
        StageConfig,
        TrainingConfig,
        CheckpointCadence,
    )

    run_kwargs = dict(
        seed=7,
        precision="float64",
        device="cpu",
        strict_cpu_determinism=False,
    )
    run_kwargs.update(run_overrides)
    # Nested overrides for guards/checkpoint if passed as objects.
    return TrainingConfig(
        stage=StageConfig(
            max_epochs=4,
            n_adam=2,
            stagnation_window=10,
            percentile_10_relaxation=0.1,
        ),
        run=RunConfig(**run_kwargs),
        opt=OptConfig(validation_every=1),
        loss=LossConfig(),
    )


def _make_arch(*, seed=7):
    from pinn.architecture_spec import ArchitectureSpec

    return ArchitectureSpec(seed=seed)


def _envelope(config, arch, *, effective_runtime_spec=None):
    build_env = _require("build_config_identity_envelope")
    return build_env(
        config, arch, effective_runtime_spec=effective_runtime_spec
    )


class IdentityPayloadTests(unittest.TestCase):
    def setUp(self):
        self.build = _require("build_identity_payload")
        self.digest = _require("identity_digest")
        self.config = _make_config()
        self.arch = _make_arch()

    def test_returns_named_dict_not_digest_string(self):
        payload = self.build(self.config, self.arch)
        self.assertIsInstance(payload, dict)
        self.assertNotIsInstance(payload, str)
        self.assertIn("run.seed", payload)
        self.assertIn("arch.hidden_depth", payload)
        self.assertIn("constants.D", payload)
        self.assertIn("effective_runtime.precision", payload)

    def test_digest_stable_for_identical(self):
        p1 = self.build(self.config, self.arch)
        p2 = self.build(self.config, self.arch)
        self.assertEqual(self.digest(p1), self.digest(p2))

    def test_digest_changes_on_arch_seed(self):
        p1 = self.build(self.config, self.arch)
        p2 = self.build(self.config, _make_arch(seed=99))
        self.assertNotEqual(self.digest(p1), self.digest(p2))

    def test_digest_changes_on_physics_constant(self):
        p1 = self.build(self.config, self.arch)
        with mock.patch(
            "pinn.training.resume.D_CHARACTERISTIC_LENGTH", 9.99
        ):
            p2 = self.build(self.config, self.arch)
        self.assertNotEqual(self.digest(p1), self.digest(p2))

    def test_digest_changes_on_effective_runtime(self):
        from pinn.runtime import resolve_runtime

        p1 = self.build(
            self.config, self.arch, effective_runtime_spec=resolve_runtime("float64", "cpu")
        )
        # Force a different effective runtime dict.
        p2 = self.build(
            self.config,
            self.arch,
            effective_runtime_spec={"precision": "float32", "device": "mps"},
        )
        self.assertNotEqual(self.digest(p1), self.digest(p2))


class NamedDiffFailSafeTests(unittest.TestCase):
    def setUp(self):
        self.diff = _require("resume_config_diff")
        self.Refused = _require("ResumeConfigRefused")
        self.config = _make_config()
        self.arch = _make_arch()
        self.stored = _envelope(self.config, self.arch)

    def test_identity_seed_change_refuses_naming_field(self):
        incoming = _make_config(seed=999)
        with self.assertRaises(self.Refused) as ctx:
            self.diff(incoming, self.arch, self.stored)
        self.assertIn("seed", str(ctx.exception))

    def test_identity_precision_change_refuses(self):
        # precision alone invalid with device=cpu; use float32/mps pair.
        incoming = _make_config(precision="float32", device="mps")
        with self.assertRaises(self.Refused) as ctx:
            self.diff(incoming, self.arch, self.stored)
        msg = str(ctx.exception)
        self.assertTrue(
            "precision" in msg or "device" in msg or "effective_runtime" in msg
        )

    def test_identity_max_epochs_change_refuses(self):
        from pinn.training.config import (
            LossConfig,
            OptConfig,
            RunConfig,
            StageConfig,
            TrainingConfig,
        )

        incoming = TrainingConfig(
            stage=StageConfig(
                max_epochs=99,
                n_adam=2,
                stagnation_window=10,
                percentile_10_relaxation=0.1,
            ),
            run=RunConfig(seed=7, precision="float64", device="cpu"),
            opt=OptConfig(validation_every=1),
            loss=LossConfig(),
        )
        with self.assertRaises(self.Refused) as ctx:
            self.diff(incoming, self.arch, self.stored)
        self.assertIn("max_epochs", str(ctx.exception))

    def test_unclassified_field_change_refuses_naming_field(self):
        # Inject an unclassified key into the stored snapshot only.
        stored = dict(self.stored)
        snap = dict(stored["resolved_config_snapshot"])
        run = dict(snap["run"])
        run["custom_debug_flag"] = 1
        snap["run"] = run
        stored["resolved_config_snapshot"] = snap
        # Digest still matches identity (unclassified not in identity payload).
        with self.assertRaises(self.Refused) as ctx:
            self.diff(self.config, self.arch, stored)
        self.assertIn("custom_debug_flag", str(ctx.exception))

    def test_operational_only_change_proceeds(self):
        from pinn.training.config import (
            CheckpointCadence,
            LossConfig,
            OptConfig,
            RunConfig,
            StageConfig,
            TrainingConfig,
        )

        # Operational: checkpoint cadence + log_every + validation_every.
        incoming = TrainingConfig(
            stage=StageConfig(
                max_epochs=4,
                n_adam=2,
                stagnation_window=10,
                percentile_10_relaxation=0.1,
            ),
            run=RunConfig(
                seed=7,
                precision="float64",
                device="cpu",
                log_every=5,
                checkpoint=CheckpointCadence(every_n_steps=50),
            ),
            opt=OptConfig(validation_every=5),
            loss=LossConfig(),
        )
        # Should not raise — operational-only drift.
        self.diff(incoming, self.arch, self.stored)


class StrictCpuIdentityClassificationTests(unittest.TestCase):
    def setUp(self):
        self.diff = _require("resume_config_diff")
        self.Refused = _require("ResumeConfigRefused")
        self.build = _require("build_identity_payload")
        self.REGISTRY = _require("RESUME_FIELD_REGISTRY")

    def test_strict_cpu_explicitly_identity_in_registry(self):
        entry = self.REGISTRY["run.strict_cpu_determinism"]
        self.assertEqual(entry["class"], "IDENTITY")

    def test_strict_flag_flip_refuses_naming_field(self):
        from pinn.runtime import resolve_runtime

        # Checkpoint taken under strict=True → effective float64/cpu.
        ckpt_cfg = _make_config(
            precision="float32",
            device="mps",
            strict_cpu_determinism=True,
        )
        arch = _make_arch()
        stored = _envelope(
            ckpt_cfg,
            arch,
            effective_runtime_spec=resolve_runtime("float64", "cpu"),
        )
        # Resume with strict=False → effective float32/mps.
        incoming = _make_config(
            precision="float32",
            device="mps",
            strict_cpu_determinism=False,
        )
        with self.assertRaises(self.Refused) as ctx:
            self.diff(
                incoming,
                arch,
                stored,
                effective_runtime_spec={"precision": "float32", "device": "mps"},
            )
        msg = str(ctx.exception)
        self.assertTrue(
            "strict_cpu_determinism" in msg or "effective_runtime" in msg,
            msg,
        )

    def test_effective_runtime_changes_when_strict_flips(self):
        from pinn.runtime import resolve_runtime

        cfg_strict = _make_config(
            precision="float32", device="mps", strict_cpu_determinism=True
        )
        cfg_loose = _make_config(
            precision="float32", device="mps", strict_cpu_determinism=False
        )
        arch = _make_arch()
        p_strict = self.build(
            cfg_strict, arch, effective_runtime_spec=resolve_runtime("float64", "cpu")
        )
        p_loose = self.build(
            cfg_loose,
            arch,
            effective_runtime_spec={"precision": "float32", "device": "mps"},
        )
        self.assertNotEqual(
            p_strict["effective_runtime.precision"],
            p_loose["effective_runtime.precision"],
        )


class DigestFastPathTests(unittest.TestCase):
    def test_matching_digest_and_snapshot_proceeds(self):
        diff = _require("resume_config_diff")
        config = _make_config()
        arch = _make_arch()
        stored = _envelope(config, arch)
        # No raise.
        diff(config, arch, stored)


class DefenseInDepthTests(unittest.TestCase):
    def test_digest_match_snapshot_mismatch_still_refuses_unclassified(self):
        diff = _require("resume_config_diff")
        Refused = _require("ResumeConfigRefused")
        config = _make_config()
        arch = _make_arch()
        stored = _envelope(config, arch)
        # Keep identity digest, mutate snapshot with unclassified key.
        snap = dict(stored["resolved_config_snapshot"])
        run = dict(snap["run"])
        run["unclassified_knob"] = "x"
        snap["run"] = run
        stored = dict(stored)
        stored["resolved_config_snapshot"] = snap
        with self.assertRaises(Refused) as ctx:
            diff(config, arch, stored)
        self.assertIn("unclassified_knob", str(ctx.exception))


class ClassificationRegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry = _require("RESUME_FIELD_REGISTRY")

    def test_covers_ctx57_identity_line(self):
        # Categories that must appear (by key prefix or exact name).
        required_substrings = [
            "arch.",
            "dataset.",
            "loss_catalog",
            "constants.",
            "run.seed",
            "run.precision",
            "run.device",
            "run.strict_cpu_determinism",
            "curriculum.",
            "split.",
            "stage.max_epochs",
            "run.guards.",
        ]
        keys = list(self.registry.keys())
        joined = " ".join(keys)
        for sub in required_substrings:
            self.assertTrue(
                any(sub in k for k in keys) or sub.rstrip(".") in joined,
                f"registry missing coverage for {sub!r}; keys={keys}",
            )

    def test_strict_cpu_explicitly_identity(self):
        self.assertEqual(
            self.registry["run.strict_cpu_determinism"]["class"], "IDENTITY"
        )

    def test_provisional_fields_registers_registry_seam(self):
        TrainingConfig = _require("TrainingConfig", CONFIG_MODULE)
        StageConfig = _require("StageConfig", CONFIG_MODULE)
        cfg = TrainingConfig(
            stage=StageConfig(
                max_epochs=4,
                n_adam=2,
                stagnation_window=10,
                percentile_10_relaxation=0.1,
            )
        )
        names = [f["name"] for f in cfg.provisional_fields()]
        self.assertIn("resume_field_classification_registry", names)
        entry = next(
            f
            for f in cfg.provisional_fields()
            if f["name"] == "resume_field_classification_registry"
        )
        self.assertTrue(entry["provisional"])
        self.assertIn("⚖", entry["provenance"])


class ResumeExactAnchorLoadingTests(unittest.TestCase):
    def setUp(self):
        self.load_resume_target = _require("load_resume_target")
        self.tmp = Path(tempfile.mkdtemp(prefix="phase41-resume-"))
        self.anchor = self.tmp / "stage-2-final.pt"
        self.anchor.write_bytes(b"placeholder")  # existence for is_file()

    def tearDown(self):
        for p in self.tmp.iterdir():
            p.unlink()
        self.tmp.rmdir()

    def test_file_routes_to_load_checkpoint_not_latest(self):
        calls = []
        anchor_payload = {"sentinel": "ANCHOR", "stage": 2}
        latest_payload = {"sentinel": "LATEST", "stage": 99}

        class FakeStore:
            def load_checkpoint(self, path):
                calls.append(("load_checkpoint", str(path)))
                return anchor_payload

            def load_latest(self):
                calls.append(("load_latest", None))
                return latest_payload

        result = self.load_resume_target(FakeStore(), self.anchor)
        self.assertEqual(result["sentinel"], "ANCHOR")
        self.assertEqual(calls[0][0], "load_checkpoint")

    def test_directory_routes_to_load_latest(self):
        calls = []

        class FakeStore:
            def load_checkpoint(self, path):
                calls.append("load_checkpoint")
                return {}

            def load_latest(self):
                calls.append("load_latest")
                return {"via": "latest"}

        result = self.load_resume_target(FakeStore(), self.tmp)
        self.assertEqual(result["via"], "latest")
        self.assertEqual(calls, ["load_latest"])

    def test_literal_latest_routes_to_load_latest(self):
        calls = []

        class FakeStore:
            def load_checkpoint(self, path):
                calls.append("load_checkpoint")
                return {}

            def load_latest(self):
                calls.append("load_latest")
                return {"via": "latest"}

        result = self.load_resume_target(FakeStore(), "latest")
        self.assertEqual(result["via"], "latest")
        self.assertEqual(calls, ["load_latest"])


class HoldStageTargetTests(unittest.TestCase):
    def setUp(self):
        self.validate = _require("validate_hold_stage_target")
        self.Err = _require("HoldStageTargetError")

    def test_accepts_stage_final(self):
        self.validate("runs/foo/checkpoints/stage-2-final.pt")

    def test_rejects_rolling(self):
        with self.assertRaises(self.Err) as ctx:
            self.validate("runs/foo/checkpoints/step-000010.pt")
        self.assertIn("step-000010.pt", str(ctx.exception))

    def test_rejects_init(self):
        with self.assertRaises(self.Err) as ctx:
            self.validate("runs/foo/checkpoints/stage-2-init.pt")
        self.assertIn("stage-2-init.pt", str(ctx.exception))

    def test_rejects_failure(self):
        with self.assertRaises(self.Err) as ctx:
            self.validate("runs/foo/checkpoints/failure-stage-2-step-5.pt")
        self.assertIn("failure", str(ctx.exception))

    def test_rejects_directory(self):
        with self.assertRaises(self.Err):
            self.validate("runs/foo/")

    def test_rejects_latest(self):
        with self.assertRaises(self.Err) as ctx:
            self.validate("latest")
        self.assertIn("latest", str(ctx.exception))


class IdentityCoverageTests(unittest.TestCase):
    def setUp(self):
        self.check = _require("identity_coverage_check")
        self.Err = _require("IdentityCoverageError")
        self.registry = _require("RESUME_FIELD_REGISTRY")
        self.build = _require("build_identity_payload")
        self.payload = self.build(_make_config(), _make_arch())

    def test_passes_dataset_free_floor(self):
        self.check(self.registry, self.payload, has_dataset=False)

    def test_raises_on_neither_coverage_tag(self):
        bad = dict(self.registry)
        bad["bogus.identity"] = {"class": "IDENTITY", "provisional": True}
        with self.assertRaises(self.Err) as ctx:
            self.check(bad, self.payload, has_dataset=False)
        self.assertIn("bogus.identity", str(ctx.exception))

    def test_raises_deferred_when_has_dataset(self):
        with self.assertRaises(self.Err) as ctx:
            self.check(self.registry, self.payload, has_dataset=True)
        msg = str(ctx.exception)
        self.assertTrue(
            "dataset" in msg or "split" in msg or "loss_catalog" in msg
            or "curriculum" in msg
        )


if __name__ == "__main__":
    unittest.main()
