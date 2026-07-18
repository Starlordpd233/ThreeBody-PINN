"""Phase 41 — atomic_io round-trip + crash-between-tmp-and-rename tests."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.phase41.test_prohibitions import _require

MODULE = "pinn.training.atomic_io"

atomic_write_text = _require("atomic_write_text", MODULE)
atomic_write_torch = _require("atomic_write_torch", MODULE)


class AtomicWriteTextTests(unittest.TestCase):
    def test_text_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hello.txt"
            atomic_write_text(path, "payload-α\n")
            self.assertTrue(path.is_file())
            self.assertEqual(path.read_text(encoding="utf-8"), "payload-α\n")

    def test_overwrite_existing_is_atomic(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cfg.yaml"
            atomic_write_text(path, "old\n")
            atomic_write_text(path, "new-content\n")
            self.assertEqual(path.read_text(encoding="utf-8"), "new-content\n")

    def test_crash_before_replace_leaves_no_canonical(self):
        """Simulated crash between tmp-write and rename: no partial at path."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "target.txt"
            # Ensure parent exists so the write reaches os.replace.
            with mock.patch("os.replace", side_effect=OSError("simulated crash")):
                with self.assertRaises(OSError):
                    atomic_write_text(path, "partial-should-not-land\n")
            self.assertFalse(
                path.exists(),
                "canonical path must not exist after a failed replace "
                "(no partial/half-written artifact)",
            )
            # Temp may be cleaned by finally; any leftover must be a .tmp.* only.
            leftovers = list(Path(tmp).iterdir())
            for leftover in leftovers:
                self.assertIn(".tmp.", leftover.name)


class AtomicWriteTorchTests(unittest.TestCase):
    def test_torch_payload_round_trip_weights_only(self):
        import torch

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.pt"
            payload = {
                "step": 7,
                "tensor": torch.tensor([1.0, 2.0, 3.0]),
                "nested": {"a": 1, "b": [1, 2]},
            }
            atomic_write_torch(path, payload)
            self.assertTrue(path.is_file())
            loaded = torch.load(path, weights_only=True)
            self.assertEqual(int(loaded["step"]), 7)
            self.assertTrue(torch.equal(loaded["tensor"], payload["tensor"]))
            self.assertEqual(loaded["nested"]["a"], 1)

    def test_torch_crash_before_replace_leaves_no_canonical(self):
        import torch

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.pt"
            with mock.patch("os.replace", side_effect=OSError("simulated crash")):
                with self.assertRaises(OSError):
                    atomic_write_torch(path, {"x": torch.tensor([1.0])})
            self.assertFalse(path.exists())


def _executable_function_source(fn) -> str:
    """Return function source with docstring and comment lines stripped."""
    import ast
    import inspect
    import textwrap

    raw = textwrap.dedent(inspect.getsource(fn))
    tree = ast.parse(raw)
    doc_lines: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc and node.body and isinstance(node.body[0], ast.Expr):
                expr = node.body[0]
                for ln in range(expr.lineno, (expr.end_lineno or expr.lineno) + 1):
                    doc_lines.add(ln)
    return "\n".join(
        line
        for ln, line in enumerate(raw.splitlines(), start=1)
        if ln not in doc_lines and line.strip() and not line.lstrip().startswith("#")
    )


class AtomicOrderingSourceTests(unittest.TestCase):
    def test_source_contains_fsync_before_replace(self):
        import inspect

        import pinn.training.atomic_io as aio

        # Public writers must fsync the temp file BEFORE rename. The helper
        # `_atomic_replace` owns the replace+dir-fsync half; each writer must
        # call file fsync before invoking it (or before os.replace).
        for name in ("atomic_write_text", "atomic_write_torch"):
            src = _executable_function_source(getattr(aio, name))
            self.assertIn("os.fsync", src, f"{name} must fsync the temp file")
            # Either direct os.replace or the shared _atomic_replace helper.
            self.assertTrue(
                "os.replace" in src or "_atomic_replace" in src,
                f"{name} must rename via os.replace or _atomic_replace",
            )
            fsync_pos = src.find("os.fsync")
            rename_pos = src.find("os.replace")
            if rename_pos < 0:
                rename_pos = src.find("_atomic_replace")
            self.assertGreater(
                rename_pos,
                fsync_pos,
                f"{name}: file fsync must precede rename (got fsync@{fsync_pos}, "
                f"rename@{rename_pos})",
            )
        # Module-level tokens required by the plan acceptance grep.
        mod_src = inspect.getsource(aio)
        self.assertIn("os.fsync", mod_src)
        self.assertIn("os.replace", mod_src)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
