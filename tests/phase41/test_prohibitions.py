"""Phase 41 mechanical boundary audit (Wave 0) — deferred-guard scaffold.

Carries the ``_require(symbol, module)`` deferred-import SkipTest helper so
downstream production symbols skip (never ERROR) until they land, plus the
CTRL-03 canon-breadcrumb prohibition scaffold (weights_only=True on every
torch.load) that arms once 41-02 lands the production CheckpointStore rewrite.
"""

from __future__ import annotations

import importlib
import inspect
import unittest

from tests.phase41 import _SKIP_PHRASE


def _require(symbol, module):
    """Per-symbol deferred import — SkipTest (never ERROR) until it lands."""
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


class RequireHelperTests(unittest.TestCase):
    """Self-check: _require skips cleanly for absent symbols (never ERROR)."""

    def test_require_skips_missing_module(self):
        with self.assertRaises(unittest.SkipTest) as ctx:
            _require("DoesNotExist", "pinn.training._phase41_absent_module_")
        self.assertIn(_SKIP_PHRASE, str(ctx.exception))

    def test_require_skips_missing_symbol(self):
        with self.assertRaises(unittest.SkipTest) as ctx:
            _require("DefinitelyNotARealSymbol_41", "pinn.training.config")
        self.assertIn(_SKIP_PHRASE, str(ctx.exception))
        self.assertIn("DefinitelyNotARealSymbol_41", str(ctx.exception))

    def test_require_returns_present_symbol(self):
        # config.TrainingConfig already exists from Phase 40.
        sym = _require("TrainingConfig", "pinn.training.config")
        self.assertTrue(callable(sym) or isinstance(sym, type))


class CheckpointWeightsOnlyProhibitionTests(unittest.TestCase):
    """CTRL-03 scaffold: every torch.load must pass weights_only=True.

    Guarded by ``_require`` so it SKIPs cleanly until 41-02 lands the
    production CheckpointStore class name in ``pinn.training.checkpoint``.
    The class name may be ``CheckpointStore`` (Protocol already present from
    Phase 40) or a later production rewrite — we audit the module source for
    the load/weights_only pairing once the production store is present.
    """

    def test_every_torch_load_uses_weights_only_true(self):
        # Phase 40 already landed CheckpointStore (Protocol) + TorchSaveCheckpointStore.
        # Arm the audit against the live module; 41-02 will keep this green.
        _require("CheckpointStore", "pinn.training.checkpoint")
        import ast

        import pinn.training.checkpoint as ckpt_mod

        # Strip docstrings so prose mentions of weights_only=True do not
        # inflate the count above the actual torch.load call sites.
        raw = inspect.getsource(ckpt_mod)
        tree = ast.parse(raw)
        doc_lines: set[int] = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                doc = ast.get_docstring(node, clean=False)
                if doc and node.body and isinstance(node.body[0], ast.Expr):
                    expr = node.body[0]
                    for ln in range(expr.lineno, (expr.end_lineno or expr.lineno) + 1):
                        doc_lines.add(ln)
        src = "\n".join(
            line
            for ln, line in enumerate(raw.splitlines(), start=1)
            if ln not in doc_lines and line.strip() and not line.lstrip().startswith("#")
        )
        load_count = src.count("torch.load")
        weights_only_count = src.count("weights_only=True")
        self.assertEqual(
            load_count,
            weights_only_count,
            "every torch.load must pass weights_only=True "
            f"(found {load_count} torch.load vs {weights_only_count} weights_only=True)",
        )


class YamlSafeLoadProhibitionTests(unittest.TestCase):
    """T-41-01: config_yaml must use yaml.safe_load exclusively (never yaml.load)."""

    def test_no_unsafe_yaml_load_in_config_yaml(self):
        # Skips until 41-01 Task 3 lands config_yaml.
        _require("load_config", "pinn.training.config_yaml")
        import inspect as _inspect

        import pinn.training.config_yaml as cy

        src = _inspect.getsource(cy)
        # Ban the unsafe call form; safe_load / safe_dump remain legal.
        # Match `yaml.load(` but not `yaml.safe_load(`.
        import re

        unsafe = re.findall(r"yaml\.load\s*\(", src)
        self.assertEqual(
            unsafe,
            [],
            "config_yaml must not call yaml.load( — use yaml.safe_load only (T-41-01)",
        )
        self.assertIn("safe_load", src)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
