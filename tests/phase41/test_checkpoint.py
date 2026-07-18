"""Phase 41 — production CheckpointStore (CTRL-02/03/04 store half).

Deferred-import via ``_require`` so missing symbols SKIP cleanly until
41-02 lands them. Covers atomic writes, weights_only loads, fallback scan,
exact-path load_checkpoint, dual-trigger cadence, retention, anchors, and
the curriculum.jsonl disposition ledger.
"""
from __future__ import annotations

import inspect
import json
import os
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any

from tests.phase41._fixtures import StubClock, StubStepCounter
from tests.phase41.test_prohibitions import _require

MODULE = "pinn.training.checkpoint"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _store_cls():
    return _require("TorchSaveCheckpointStore", MODULE)


def _empty_exc():
    return _require("EmptyCheckpointStore", MODULE)


def _no_valid():
    return _require("NoValidCheckpointError", MODULE)


def _schema_version():
    return _require("CHECKPOINT_SCHEMA_VERSION", MODULE)


def _protocol():
    return _require("CheckpointStore", MODULE)


def _make_ctx53_payload(**overrides: Any) -> dict:
    """Minimal plain CTX-53 nested dict (weights_only-clean)."""
    import torch

    base = {
        "model": {"w": torch.tensor([1.0, 2.0], dtype=torch.float32)},
        "optimizer": None,  # stage-init may carry None — presence, not truthiness
        "scheduled_weights": {"lambda_e": 0.1},
        "grad_clip": {"C": 1.0},
        "curriculum": {"stage": 0, "phase": "2a"},
        "rng": {"torch": [1, 2, 3]},
        "counters": {"global_step": 0, "epoch": 0},
        "config_identity": {"digest": "abc", "config": {"seed": 0}},
        "schema_version": _schema_version(),
    }
    base.update(overrides)
    return base


def _make_store(td: str, **kwargs: Any):
    cls = _store_cls()
    from pinn.training.config import CheckpointCadence

    cadence = kwargs.pop("cadence", None)
    if cadence is None:
        cadence = CheckpointCadence(
            every_n_steps=kwargs.pop("every_n_steps", 10),
            wall_clock_ceiling_s=kwargs.pop("wall_clock_ceiling_s", 100.0),
            rolling_keep=kwargs.pop("rolling_keep", 3),
            failure_keep=kwargs.pop("failure_keep", 3),
        )
    else:
        kwargs.pop("every_n_steps", None)
        kwargs.pop("wall_clock_ceiling_s", None)
        kwargs.pop("rolling_keep", None)
        kwargs.pop("failure_keep", None)
    return cls(td, cadence=cadence, **kwargs)


# ===========================================================================
# Task 1 — CTRL-03
# ===========================================================================


class ProtocolShapeTests(unittest.TestCase):
    def test_protocol_members(self):
        proto = _protocol()
        self.assertTrue(hasattr(proto, "save"))
        self.assertTrue(hasattr(proto, "load_latest"))
        self.assertTrue(hasattr(proto, "rollback"))

    def test_production_satisfies_protocol_methods(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            self.assertTrue(callable(store.save))
            self.assertTrue(callable(store.load_latest))
            self.assertTrue(callable(store.rollback))

    def test_empty_store_raises_on_load_latest(self):
        Empty = _empty_exc()
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            with self.assertRaises(Empty):
                store.load_latest()

    def test_empty_store_raises_on_rollback(self):
        Empty = _empty_exc()
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            with self.assertRaises(Empty):
                store.rollback()

    def test_disposition_noop_defaults_on_empty_store_class(self):
        """HIGH 5: EmptyCheckpointStore constructible as no-op store."""
        Empty = _empty_exc()
        empty = Empty()
        # record_disposition / promote must not raise
        self.assertFalse(empty.record_disposition(0, 1, "ADVANCE", 0))
        empty.promote(0, 1)  # no-op, no raise
        self.assertIsNone(empty.save_anchor("stage-0-final", 0, {}))
        rr = empty.save_rolling({}, 1)
        self.assertTrue(rr is None or rr == "")
        br = empty.save_best({})
        self.assertTrue(br is None or br == "")

    def test_disposition_methods_on_production_store(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            # Production may no-op or implement; must not AttributeError
            self.assertTrue(hasattr(store, "save_anchor"))
            self.assertTrue(hasattr(store, "record_disposition"))
            self.assertTrue(hasattr(store, "promote"))
            self.assertTrue(hasattr(store, "load_checkpoint"))
            self.assertTrue(hasattr(store, "save_rolling"))
            self.assertTrue(hasattr(store, "save_best"))


class RoundTripTests(unittest.TestCase):
    def test_ctx53_payload_round_trips_weights_only(self):
        import torch

        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            payload = _make_ctx53_payload()
            cid = store.save(payload)
            self.assertTrue(cid)
            loaded = store.load_latest()
            self.assertEqual(loaded["schema_version"], _schema_version())
            self.assertEqual(loaded["curriculum"]["stage"], 0)
            self.assertTrue(
                torch.allclose(loaded["model"]["w"], payload["model"]["w"])
            )
            # weights_only path: re-load file directly
            latest = Path(td) / "latest.pt"
            direct = torch.load(latest, weights_only=True)
            self.assertEqual(direct["config_identity"]["digest"], "abc")

    def test_optimizer_none_is_structurally_valid(self):
        """Presence not truthiness — optimizer: None is valid (CTRL-06 stage-init)."""
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            payload = _make_ctx53_payload(optimizer=None)
            store.save_rolling(payload, step=1)
            # corrupt latest so fallback runs
            (Path(td) / "latest.pt").write_bytes(b"not-a-checkpoint")
            recovered = store.fallback_scan()
            self.assertIsNone(recovered["optimizer"])
            self.assertIn("optimizer", recovered)


class AtomicityTests(unittest.TestCase):
    def test_os_replace_failure_leaves_no_canonical(self):
        import pinn.training.atomic_io as atomic_io

        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            payload = _make_ctx53_payload()
            canonical = Path(td) / "latest.pt"
            real_replace = os.replace

            def boom(src, dst):
                raise OSError("simulated crash before rename")

            original = atomic_io.os.replace
            try:
                atomic_io.os.replace = boom  # type: ignore[assignment]
                with self.assertRaises(OSError):
                    store.save(payload)
            finally:
                atomic_io.os.replace = original  # type: ignore[assignment]

            self.assertFalse(
                canonical.exists(),
                "canonical latest.pt must not exist after crash-before-rename",
            )
            # No half-written .pt under canonical names
            leftovers = [
                p
                for p in Path(td).iterdir()
                if p.suffix == ".pt" and ".tmp." not in p.name
            ]
            self.assertEqual(leftovers, [])


class FallbackScanTests(unittest.TestCase):
    def test_corrupt_latest_falls_back_to_valid_step(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            good = _make_ctx53_payload(counters={"global_step": 5, "epoch": 1})
            store.save_rolling(good, step=5)
            # Corrupt latest.pt
            (Path(td) / "latest.pt").write_bytes(b"truncated-garbage")
            loaded = store.load_latest()
            self.assertEqual(loaded["counters"]["global_step"], 5)

    def test_skips_missing_required_key(self):
        import torch

        from pinn.training.atomic_io import atomic_write_torch

        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            # Write a step file missing config_identity
            bad = _make_ctx53_payload()
            del bad["config_identity"]
            atomic_write_torch(Path(td) / "step-000010.pt", bad)
            # And a valid older one
            good = _make_ctx53_payload(counters={"global_step": 3, "epoch": 0})
            atomic_write_torch(Path(td) / "step-000003.pt", good)
            (Path(td) / "latest.pt").write_bytes(b"corrupt")
            loaded = store.fallback_scan()
            self.assertEqual(loaded["counters"]["global_step"], 3)

    def test_skips_stale_schema_version(self):
        from pinn.training.atomic_io import atomic_write_torch

        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            stale = _make_ctx53_payload(schema_version=0)
            atomic_write_torch(Path(td) / "step-000099.pt", stale)
            good = _make_ctx53_payload(counters={"global_step": 1, "epoch": 0})
            atomic_write_torch(Path(td) / "step-000001.pt", good)
            (Path(td) / "latest.pt").write_bytes(b"corrupt")
            loaded = store.fallback_scan()
            self.assertEqual(loaded["counters"]["global_step"], 1)

    def test_no_valid_candidate_raises_naming_dir(self):
        NoValid = _no_valid()
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            (Path(td) / "latest.pt").write_bytes(b"corrupt")
            with self.assertRaises(NoValid) as ctx:
                store.fallback_scan()
            self.assertIn(td, str(ctx.exception))

    def test_failure_anchor_excluded_even_when_newest(self):
        """LOW-2: never auto-resume from a structurally-valid failure-*."""
        from pinn.training.atomic_io import atomic_write_torch

        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            older = _make_ctx53_payload(
                counters={"global_step": 2, "epoch": 0},
                curriculum={"stage": 0, "phase": "2a", "tag": "rolling"},
            )
            atomic_write_torch(Path(td) / "step-000002.pt", older)
            # Newer, valid failure anchor
            fail = _make_ctx53_payload(
                counters={"global_step": 99, "epoch": 9},
                curriculum={"stage": 0, "phase": "2a", "tag": "failure"},
            )
            atomic_write_torch(Path(td) / "failure-stage-0-step-99.pt", fail)
            (Path(td) / "latest.pt").write_bytes(b"corrupt")
            loaded = store.fallback_scan()
            self.assertEqual(loaded["counters"]["global_step"], 2)
            self.assertEqual(loaded["curriculum"]["tag"], "rolling")


class LoadCheckpointTests(unittest.TestCase):
    def test_exact_path_not_latest(self):
        from pinn.training.atomic_io import atomic_write_torch

        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            anchor = _make_ctx53_payload(
                curriculum={"stage": 1, "phase": "2a", "sentinel": "ANCHOR"}
            )
            latest_p = _make_ctx53_payload(
                curriculum={"stage": 2, "phase": "2b", "sentinel": "LATEST"}
            )
            anchor_path = Path(td) / "stage-1-final.pt"
            atomic_write_torch(anchor_path, anchor)
            atomic_write_torch(Path(td) / "latest.pt", latest_p)
            loaded = store.load_checkpoint(anchor_path)
            self.assertEqual(loaded["curriculum"]["sentinel"], "ANCHOR")
            self.assertNotEqual(loaded["curriculum"]["sentinel"], "LATEST")

    def test_path_escape_relative(self):
        NoValid = _no_valid()
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            evil = Path(td) / ".." / "evil.pt"
            with self.assertRaises(NoValid) as ctx:
                store.load_checkpoint(evil)
            self.assertTrue(
                "evil" in str(ctx.exception) or ".." in str(ctx.exception)
                or str(evil) in str(ctx.exception)
                or "no valid" in str(ctx.exception).lower()
            )

    def test_path_escape_absolute_outside(self):
        NoValid = _no_valid()
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            outside = Path("/tmp/phase41_evil_checkpoint.pt")
            with self.assertRaises(NoValid) as ctx:
                store.load_checkpoint(outside)
            self.assertIn(str(outside), str(ctx.exception))

    def test_missing_file_raises_naming_path(self):
        NoValid = _no_valid()
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            missing = Path(td) / "stage-0-final.pt"
            with self.assertRaises(NoValid) as ctx:
                store.load_checkpoint(missing)
            self.assertIn(str(missing), str(ctx.exception))

    def test_schema_mismatch_raises(self):
        from pinn.training.atomic_io import atomic_write_torch

        NoValid = _no_valid()
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            bad = _make_ctx53_payload(schema_version=0)
            path = Path(td) / "stage-0-final.pt"
            atomic_write_torch(path, bad)
            with self.assertRaises(NoValid) as ctx:
                store.load_checkpoint(path)
            self.assertIn(str(path), str(ctx.exception))

    def test_missing_required_key_raises(self):
        from pinn.training.atomic_io import atomic_write_torch

        NoValid = _no_valid()
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            bad = _make_ctx53_payload()
            del bad["rng"]
            path = Path(td) / "stage-0-final.pt"
            atomic_write_torch(path, bad)
            with self.assertRaises(NoValid) as ctx:
                store.load_checkpoint(path)
            self.assertIn(str(path), str(ctx.exception))

    def test_empty_store_load_checkpoint_raises(self):
        Empty = _empty_exc()
        NoValid = _no_valid()
        empty = Empty()
        with self.assertRaises(NoValid) as ctx:
            empty.load_checkpoint("/any/path.pt")
        self.assertIn("/any/path.pt", str(ctx.exception))


class WeightsOnlyProhibitionTests(unittest.TestCase):
    def test_every_torch_load_uses_weights_only(self):
        cls = _store_cls()
        src = inspect.getsource(cls)
        self.assertIn("weights_only=True", src)
        self.assertEqual(
            src.count("torch.load"),
            src.count("weights_only=True"),
            "every torch.load must pass weights_only=True (no escape hatch)",
        )
        self.assertNotIn("weights_only=False", src)


# ===========================================================================
# Task 2 — CTRL-02 dual trigger + retention
# ===========================================================================


class DualTriggerTests(unittest.TestCase):
    def test_step_trigger_fires(self):
        clock = StubClock(0.0)
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(
                td, every_n_steps=10, wall_clock_ceiling_s=1000.0, clock=clock.now
            )
            self.assertFalse(store.should_checkpoint(1, elapsed=0.0))
            self.assertTrue(store.should_checkpoint(10, elapsed=0.0))

    def test_wall_clock_ceiling_fires_first(self):
        clock = StubClock(0.0)
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(
                td, every_n_steps=100, wall_clock_ceiling_s=50.0, clock=clock.now
            )
            # Not on step boundary; elapsed past ceiling
            self.assertTrue(store.should_checkpoint(7, elapsed=50.0))

    def test_coincident_fires_exactly_once(self):
        clock = StubClock(0.0)
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(
                td, every_n_steps=10, wall_clock_ceiling_s=50.0, clock=clock.now
            )
            step = 10
            elapsed = 50.0
            self.assertTrue(store.should_checkpoint(step, elapsed))
            # Simulate a write advancing last_written_*
            store.save_rolling(_make_ctx53_payload(), step=step)
            # Same step must not re-fire
            self.assertFalse(store.should_checkpoint(step, elapsed=50.0))

    def test_after_wall_clock_write_next_step_does_not_retrigger(self):
        """CYCLE-2 HIGH 3: elapsed resets via last_written_time advance."""
        clock = StubClock(0.0)
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(
                td, every_n_steps=100, wall_clock_ceiling_s=30.0, clock=clock.now
            )
            clock.set(35.0)
            elapsed = clock.now() - store.last_written_time
            self.assertTrue(store.should_checkpoint(3, elapsed=elapsed))
            store.save_rolling(_make_ctx53_payload(), step=3)
            # Advance only the step counter; clock stays put → elapsed ≈ 0
            elapsed2 = clock.now() - store.last_written_time
            self.assertLess(elapsed2, 30.0)
            self.assertFalse(store.should_checkpoint(4, elapsed=elapsed2))

    def test_default_clock_is_time_monotonic(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            # Production default is time.monotonic, never time.time
            self.assertIs(store._clock, time.monotonic)


class RetentionTests(unittest.TestCase):
    def test_rolling_keeps_newest_n(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td, rolling_keep=3, every_n_steps=1)
            for step in (1, 2, 3, 4, 5):
                store.save_rolling(_make_ctx53_payload(), step=step)
            steps = sorted(
                int(p.stem.split("-")[1])
                for p in Path(td).glob("step-*.pt")
            )
            self.assertEqual(steps, [3, 4, 5])

    def test_best_latest_anchors_survive_rolling(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td, rolling_keep=2)
            store.save_best(_make_ctx53_payload(curriculum={"stage": 0, "tag": "best"}))
            store.save_anchor(
                "stage-0-final",
                0,
                _make_ctx53_payload(curriculum={"stage": 0, "tag": "final"}),
            )
            for step in (1, 2, 3, 4):
                store.save_rolling(_make_ctx53_payload(), step=step)
            self.assertTrue((Path(td) / "best.pt").is_file())
            self.assertTrue((Path(td) / "latest.pt").is_file())
            self.assertTrue((Path(td) / "stage-0-final.pt").is_file())
            # latest is a real file copy, not a symlink
            self.assertFalse((Path(td) / "latest.pt").is_symlink())

    def test_save_best_does_not_refresh_latest(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            rolling = _make_ctx53_payload(
                curriculum={"stage": 0, "sentinel": "ROLLING"}
            )
            store.save_rolling(rolling, step=1)
            best = _make_ctx53_payload(curriculum={"stage": 0, "sentinel": "BEST"})
            store.save_best(best)
            import torch

            latest = torch.load(Path(td) / "latest.pt", weights_only=True)
            self.assertEqual(latest["curriculum"]["sentinel"], "ROLLING")

    def test_save_rolling_does_refresh_latest(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            p = _make_ctx53_payload(curriculum={"stage": 0, "sentinel": "R2"})
            store.save_rolling(p, step=2)
            import torch

            latest = torch.load(Path(td) / "latest.pt", weights_only=True)
            self.assertEqual(latest["curriculum"]["sentinel"], "R2")

    def test_fewer_than_keep_deletes_nothing(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td, rolling_keep=3)
            store.save_rolling(_make_ctx53_payload(), step=1)
            store.save_rolling(_make_ctx53_payload(), step=2)
            steps = list(Path(td).glob("step-*.pt"))
            self.assertEqual(len(steps), 2)

    def test_ceiling_from_config_not_inlined(self):
        from pinn.training.config import CheckpointCadence

        cadence = CheckpointCadence(
            every_n_steps=7,
            wall_clock_ceiling_s=12.5,
            rolling_keep=3,
            failure_keep=5,
        )
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td, cadence=cadence)
            self.assertEqual(store._wall_clock_ceiling_s, 12.5)
            self.assertEqual(store._every_n_steps, 7)
            # Not an inlined ratified constant in the store class body
            src = inspect.getsource(_store_cls())
            # Store should read ceiling from cadence/config, not hard-code 3600
            # (provisional default lives in config.py, not checkpoint.py)
            self.assertNotIn("3600", src)


class FailureRetentionTests(unittest.TestCase):
    def test_failure_keep_evicts_oldest(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td, failure_keep=2)
            for step in (1, 2, 3, 4):
                store.save_anchor(
                    f"failure-stage-0-step-{step}",
                    0,
                    _make_ctx53_payload(),
                )
            fails = sorted(Path(td).glob("failure-*.pt"))
            self.assertEqual(len(fails), 2)
            names = {p.name for p in fails}
            self.assertIn("failure-stage-0-step-3.pt", names)
            self.assertIn("failure-stage-0-step-4.pt", names)
            self.assertNotIn("failure-stage-0-step-1.pt", names)

    def test_failure_does_not_refresh_latest(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            store.save_rolling(
                _make_ctx53_payload(curriculum={"stage": 0, "sentinel": "ROLL"}),
                step=1,
            )
            store.save_anchor(
                "failure-stage-0-step-9",
                0,
                _make_ctx53_payload(curriculum={"stage": 0, "sentinel": "FAIL"}),
            )
            import torch

            latest = torch.load(Path(td) / "latest.pt", weights_only=True)
            self.assertEqual(latest["curriculum"]["sentinel"], "ROLL")

    def test_failure_retention_leaves_stage_and_rolling(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td, failure_keep=1, rolling_keep=3)
            store.save_rolling(_make_ctx53_payload(), step=1)
            store.save_anchor(
                "stage-0-final", 0, _make_ctx53_payload()
            )
            store.save_anchor("failure-stage-0-step-1", 0, _make_ctx53_payload())
            store.save_anchor("failure-stage-0-step-2", 0, _make_ctx53_payload())
            self.assertTrue((Path(td) / "step-000001.pt").is_file())
            self.assertTrue((Path(td) / "stage-0-final.pt").is_file())
            self.assertTrue((Path(td) / "failure-stage-0-step-2.pt").is_file())
            self.assertFalse((Path(td) / "failure-stage-0-step-1.pt").is_file())


# ===========================================================================
# Task 3 — CTRL-04 anchors + promotion + ledger
# ===========================================================================


class AnchorTests(unittest.TestCase):
    def test_stage_anchors_written_and_survive_rolling(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td, rolling_keep=2)
            store.save_anchor("stage-0-final", 0, _make_ctx53_payload())
            store.save_anchor("stage-1-init", 1, _make_ctx53_payload())
            for step in (1, 2, 3, 4):
                store.save_rolling(_make_ctx53_payload(), step=step)
            self.assertTrue((Path(td) / "stage-0-final.pt").is_file())
            self.assertTrue((Path(td) / "stage-1-init.pt").is_file())

    def test_replayed_anchor_is_noop(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            p1 = _make_ctx53_payload(curriculum={"stage": 0, "sentinel": "FIRST"})
            p2 = _make_ctx53_payload(curriculum={"stage": 0, "sentinel": "SECOND"})
            r1 = store.save_anchor("stage-0-final", 0, p1)
            self.assertIsNotNone(r1)
            mtime1 = (Path(td) / "stage-0-final.pt").stat().st_mtime_ns
            r2 = store.save_anchor("stage-0-final", 0, p2)
            self.assertIsNone(r2)
            mtime2 = (Path(td) / "stage-0-final.pt").stat().st_mtime_ns
            self.assertEqual(mtime1, mtime2)
            import torch

            loaded = torch.load(Path(td) / "stage-0-final.pt", weights_only=True)
            self.assertEqual(loaded["curriculum"]["sentinel"], "FIRST")

    def test_init_anchor_refreshes_latest(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            store.save_rolling(
                _make_ctx53_payload(curriculum={"stage": 0, "sentinel": "OLD"}),
                step=1,
            )
            store.save_anchor(
                "stage-1-init",
                1,
                _make_ctx53_payload(curriculum={"stage": 1, "sentinel": "INIT"}),
            )
            import torch

            latest = torch.load(Path(td) / "latest.pt", weights_only=True)
            self.assertEqual(latest["curriculum"]["sentinel"], "INIT")

    def test_failure_anchor_does_not_refresh_latest(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            store.save_rolling(
                _make_ctx53_payload(curriculum={"stage": 0, "sentinel": "ROLL"}),
                step=1,
            )
            store.save_anchor(
                "failure-stage-0-step-5",
                0,
                _make_ctx53_payload(curriculum={"stage": 0, "sentinel": "FAIL"}),
            )
            import torch

            latest = torch.load(Path(td) / "latest.pt", weights_only=True)
            self.assertEqual(latest["curriculum"]["sentinel"], "ROLL")

    def test_replayed_failure_anchor_noop(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            r1 = store.save_anchor(
                "failure-stage-0-step-1", 0, _make_ctx53_payload()
            )
            r2 = store.save_anchor(
                "failure-stage-0-step-1", 0, _make_ctx53_payload()
            )
            self.assertIsNotNone(r1)
            self.assertIsNone(r2)


class PromotionLedgerTests(unittest.TestCase):
    def test_promote_accepts_k_to_k_plus_1(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td, terminal_stage=2)
            self.assertTrue(store.promote(0, 1))
            self.assertTrue(store.promote(1, 2))

    def test_promote_refuses_skip(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td, terminal_stage=2)
            with self.assertRaises(Exception) as ctx:
                store.promote(0, 2)
            msg = str(ctx.exception)
            self.assertTrue("0" in msg and "2" in msg)

    def test_promote_refuses_regress(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td, terminal_stage=2)
            with self.assertRaises(Exception) as ctx:
                store.promote(2, 1)
            msg = str(ctx.exception)
            self.assertTrue("2" in msg and "1" in msg)

    def test_promote_refuses_beyond_terminal(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td, terminal_stage=2)
            with self.assertRaises(Exception) as ctx:
                store.promote(2, 3)
            msg = str(ctx.exception)
            self.assertTrue("2" in msg and "3" in msg)

    def test_record_disposition_appends_one_line(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            self.assertTrue(
                store.record_disposition(0, 1, "ADVANCE", 10)
            )
            self.assertTrue(
                store.record_disposition(1, 1, "RECOVER", 20)
            )
            self.assertTrue(
                store.record_disposition(1, 1, "HALT", 30)
            )
            ledger = Path(td).parent / "curriculum.jsonl"
            # store root is checkpoints/; ledger is sibling under run root
            # When root IS the temp dir used as checkpoints, parent is temp's parent.
            # Our store puts ledger at root.parent / curriculum.jsonl when root
            # is checkpoints/, but tests pass td as root directly.
            # Accept either root/curriculum.jsonl or root.parent/curriculum.jsonl
            candidates = [
                Path(td) / "curriculum.jsonl",
                Path(td).parent / "curriculum.jsonl",
            ]
            ledger_path = next((p for p in candidates if p.is_file()), None)
            self.assertIsNotNone(ledger_path, "curriculum.jsonl not found")
            lines = ledger_path.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 3)
            parsed = [json.loads(line) for line in lines]
            self.assertEqual(parsed[0]["disposition"], "ADVANCE")
            self.assertEqual(parsed[1]["disposition"], "RECOVER")
            self.assertEqual(parsed[2]["disposition"], "HALT")
            for row in parsed:
                for key in ("from_stage", "to_stage", "disposition", "step"):
                    self.assertIn(key, row)

    def test_record_disposition_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            self.assertTrue(store.record_disposition(0, 1, "ADVANCE", 10))
            self.assertFalse(store.record_disposition(0, 1, "ADVANCE", 10))
            candidates = [
                Path(td) / "curriculum.jsonl",
                Path(td).parent / "curriculum.jsonl",
            ]
            ledger_path = next((p for p in candidates if p.is_file()), None)
            self.assertIsNotNone(ledger_path)
            lines = ledger_path.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 1)

    def test_fresh_run_well_formed_empty_ledger(self):
        with tempfile.TemporaryDirectory() as td:
            store = _make_store(td)
            # No dispositions yet — ledger may be absent or empty; both well-formed
            candidates = [
                Path(td) / "curriculum.jsonl",
                Path(td).parent / "curriculum.jsonl",
            ]
            existing = [p for p in candidates if p.is_file()]
            for p in existing:
                content = p.read_text(encoding="utf-8")
                if content.strip():
                    for line in content.strip().splitlines():
                        json.loads(line)  # must be valid JSON


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
