"""Phase 40 — CheckpointStore protocol + naive torch.save impl (CTX-43/44).

weights_only=True on every load/rollback (T-40-02 closed now, not deferred).
Empty store raises EmptyCheckpointStore.
"""
from __future__ import annotations

import inspect
import tempfile
import unittest
from pathlib import Path

from tests.phase40.test_prohibitions import _require

MODULE = "pinn.training.checkpoint"

CheckpointStore = _require("CheckpointStore", MODULE)
TorchSaveCheckpointStore = _require("TorchSaveCheckpointStore", MODULE)
EmptyCheckpointStore = _require("EmptyCheckpointStore", MODULE)


class ProtocolShapeTests(unittest.TestCase):
    def test_protocol_members(self):
        self.assertTrue(hasattr(CheckpointStore, "save"))
        self.assertTrue(hasattr(CheckpointStore, "load_latest"))
        self.assertTrue(hasattr(CheckpointStore, "rollback"))

    def test_naive_impl_is_instance(self):
        import typing
        with tempfile.TemporaryDirectory() as td:
            store = TorchSaveCheckpointStore(td)
            # Structural: runtime_checkable if marked; else duck-type methods.
            self.assertTrue(callable(store.save))
            self.assertTrue(callable(store.load_latest))
            self.assertTrue(callable(store.rollback))
            if getattr(CheckpointStore, "_is_runtime_protocol", False) or hasattr(
                typing, "runtime_checkable"
            ):
                try:
                    self.assertIsInstance(store, CheckpointStore)
                except TypeError:
                    pass  # non-runtime Protocol is fine


class RoundTripTests(unittest.TestCase):
    def test_save_load_latest_nested_tensors(self):
        import torch

        with tempfile.TemporaryDirectory() as td:
            store = TorchSaveCheckpointStore(td)
            state = {
                "model": {
                    "w": torch.tensor([1.0, 2.0, 3.0], dtype=torch.float64),
                    "b": torch.tensor(0.5, dtype=torch.float64),
                },
                "opt": {"step": 7},
                "scalar": 3.14,
            }
            cid = store.save(state)
            self.assertTrue(cid)
            loaded = store.load_latest()
            self.assertEqual(loaded["opt"]["step"], 7)
            self.assertEqual(loaded["scalar"], 3.14)
            self.assertTrue(torch.allclose(loaded["model"]["w"], state["model"]["w"]))
            self.assertTrue(torch.allclose(loaded["model"]["b"], state["model"]["b"]))

    def test_rollback_returns_last_well_formed(self):
        import torch

        with tempfile.TemporaryDirectory() as td:
            store = TorchSaveCheckpointStore(td)
            s1 = {"v": torch.tensor([1.0])}
            s2 = {"v": torch.tensor([2.0])}
            store.save(s1)
            store.save(s2)
            rb = store.rollback()
            self.assertTrue(torch.allclose(rb["v"], s2["v"]))


class EmptyStoreTests(unittest.TestCase):
    def test_load_latest_empty_raises(self):
        with tempfile.TemporaryDirectory() as td:
            store = TorchSaveCheckpointStore(td)
            with self.assertRaises(EmptyCheckpointStore):
                store.load_latest()

    def test_rollback_empty_raises(self):
        with tempfile.TemporaryDirectory() as td:
            store = TorchSaveCheckpointStore(td)
            with self.assertRaises(EmptyCheckpointStore):
                store.rollback()


class WeightsOnlyAndPayloadTests(unittest.TestCase):
    def test_load_path_uses_weights_only(self):
        src = inspect.getsource(TorchSaveCheckpointStore)
        self.assertIn("weights_only=True", src)
        # Every torch.load call must pass the flag.
        self.assertEqual(src.count("torch.load"), src.count("weights_only=True"))

    def test_payload_plain_types_only(self):
        import torch

        with tempfile.TemporaryDirectory() as td:
            store = TorchSaveCheckpointStore(td)
            state = {
                "t": torch.zeros(2),
                "n": 1,
                "f": 1.5,
                "s": "ok",
                "nested": {"a": [1, 2, 3]},
            }
            store.save(state)
            loaded = store.load_latest()
            self._assert_plain(loaded)

    def _assert_plain(self, obj):
        import torch

        if isinstance(obj, torch.Tensor):
            return
        if isinstance(obj, (int, float, str, bool, type(None))):
            return
        if isinstance(obj, dict):
            for k, v in obj.items():
                self.assertIsInstance(k, (str, int))
                self._assert_plain(v)
            return
        if isinstance(obj, (list, tuple)):
            for v in obj:
                self._assert_plain(v)
            return
        self.fail(f"non-plain payload type: {type(obj)!r}")


if __name__ == "__main__":
    unittest.main()
