"""Phase 37 ENV-04 runtime-profile seam test contract (CTX-12..CTX-14 / T-37-05).

Wave 0 contract. Tests import ``pinn.runtime`` inside test methods so module
compilation is the only Wave 0 green condition; the suite turns green only in
Wave 2 when the resolver lands.
"""

import importlib
import unittest

ROOT_IMPORT = "pinn.runtime"


def _load_runtime():
    """Import the production runtime module; skip the test if it does not exist yet.

    Wave 0 leaves this RED (skipped via fail-fast) until Wave 2 implements
    ``pinn/runtime.py``. Tests below call this inside test methods so module
    compilation is the only Wave 0 green condition.
    """
    try:
        module = importlib.import_module(ROOT_IMPORT)
    except ImportError as exc:
        raise unittest.SkipTest(f"pinn.runtime not implemented until Wave 2: {exc}")
    return module


def _load_torch():
    """Import torch; skip cleanly if it is not installed.

    Production-target tests need torch only after ``pinn.runtime`` exists
    (Wave 2+). On a host without torch (the Wave 0 environment), every
    torch-dependent test must SKIP rather than ERROR — the Wave 0 contract is
    "intentionally RED only on later-wave production targets", and an
    ImportError from a missing dependency is an environment failure, not a
    production-target miss.
    """
    try:
        import torch
    except ImportError as exc:
        raise unittest.SkipTest(f"torch not installed until Wave 1 creates pinn-train: {exc}")
    return torch


class RuntimeResolverTests(unittest.TestCase):
    """CTX-12..CTX-14: exactly two profile pairs, fail-closed on the rest."""

    def test_float32_mps_resolves_to_required_dtype_and_device(self):
        torch = _load_torch()
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float32", "mps")
        self.assertEqual(spec.dtype, torch.float32)
        # Requested device is 'mps'; the resolved device fact is recorded as-is
        # without availability inference (CTX-12 forbids inferring availability).
        self.assertEqual(spec.requested_device, "mps")
        self.assertEqual(spec.torch_device.type, "mps")

    def test_float64_cpu_resolves_to_required_dtype_and_device(self):
        torch = _load_torch()
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float64", "cpu")
        self.assertEqual(spec.dtype, torch.float64)
        self.assertEqual(spec.torch_device.type, "cpu")
        self.assertEqual(spec.requested_device, "cpu")

    def test_runtime_spec_is_frozen(self):
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float32", "mps")
        # Frozen dataclass / namedtuple: attribute assignment must raise.
        with self.assertRaises((AttributeError, TypeError)):
            spec.dtype = "x"
        with self.assertRaises((AttributeError, TypeError)):
            spec.requested_device = "cpu"

    def test_float64_mps_fails_before_tensor_creation(self):
        runtime = _load_runtime()
        with self.assertRaises((ValueError, TypeError)) as ctx:
            runtime.resolve_runtime("float64", "mps")
        # The error must name the two permitted pairs so the caller can recover.
        msg = str(ctx.exception)
        self.assertIn("float32", msg)
        self.assertIn("mps", msg)
        self.assertIn("float64", msg)
        self.assertIn("cpu", msg)

    def test_float32_cpu_fails_before_tensor_creation(self):
        runtime = _load_runtime()
        with self.assertRaises((ValueError, TypeError)):
            runtime.resolve_runtime("float32", "cpu")

    def test_omitted_precision_fails(self):
        runtime = _load_runtime()
        with self.assertRaises((ValueError, TypeError)):
            runtime.resolve_runtime(None, "mps")

    def test_omitted_device_fails(self):
        runtime = _load_runtime()
        with self.assertRaises((ValueError, TypeError)):
            runtime.resolve_runtime("float32", None)

    def test_unknown_precision_fails(self):
        runtime = _load_runtime()
        with self.assertRaises((ValueError, TypeError)):
            runtime.resolve_runtime("bfloat16", "mps")

    def test_unknown_device_fails(self):
        runtime = _load_runtime()
        with self.assertRaises((ValueError, TypeError)):
            runtime.resolve_runtime("float32", "cuda")

    def test_partial_pair_fails(self):
        # Only one of the two approved pairs is half-supplied; the resolver must
        # not silently accept the matching half.
        runtime = _load_runtime()
        # The approved pairs are (float32, mps) and (float64, cpu). The cross
        # pair (float32, cpu) must fail.
        with self.assertRaises((ValueError, TypeError)):
            runtime.resolve_runtime("float32", "cpu")
        with self.assertRaises((ValueError, TypeError)):
            runtime.resolve_runtime("float64", "mps")

    def test_no_resolver_call_mutates_global_default_dtype(self):
        torch = _load_torch()
        runtime = _load_runtime()
        before = torch.get_default_dtype()
        try:
            runtime.resolve_runtime("float32", "mps")
            runtime.resolve_runtime("float64", "cpu")
            for bad in (("float64", "mps"), ("float32", "cpu"), ("bfloat16", "mps")):
                try:
                    runtime.resolve_runtime(*bad)
                except (ValueError, TypeError):
                    pass
        finally:
            after = torch.get_default_dtype()
        self.assertEqual(before, after,
                         "resolve_runtime mutated the global default dtype")

    def test_resolver_does_not_infer_availability_or_retry(self):
        # CTX-12/14: no availability inference, no retry, no implicit default.
        # The resolver must not import MPS-availability probes or call them. We
        # assert by source inspection of EXECUTABLE CODE ONLY (stripping
        # docstrings and comments, which legitimately mention these tokens to
        # document that the resolver does NOT use them) that the resolver file
        # does not call torch.set_default_dtype / is_available / retry.
        import ast
        import pathlib
        repo_root = pathlib.Path(__file__).resolve().parents[2]
        runtime_py = repo_root / "pinn" / "runtime.py"
        if not runtime_py.exists():
            self.skipTest("pinn/runtime.py not implemented until Wave 2")
        source = runtime_py.read_text()
        tree = ast.parse(source, filename=str(runtime_py))
        # Collect line numbers of docstring and comment spans so we can exclude
        # them from the executable-code scan.
        docstring_lines = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.ClassDef, ast.Module)):
                doc = ast.get_docstring(node, clean=False)
                if doc and node.body and isinstance(node.body[0], ast.Expr):
                    expr = node.body[0]
                    if hasattr(expr, "lineno") and hasattr(expr, "end_lineno"):
                        for ln in range(expr.lineno, (expr.end_lineno or expr.lineno) + 1):
                            docstring_lines.add(ln)
        executable_lines = []
        for ln, line in enumerate(source.splitlines(), 1):
            if ln in docstring_lines:
                continue
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            executable_lines.append(stripped)
        executable = "\n".join(executable_lines)
        self.assertNotIn("torch.set_default_dtype", executable,
                         "resolver mutates global default dtype")
        self.assertNotIn("is_available", executable,
                         "resolver performs availability inference")
        # "retry" as a word in executable code would indicate a retry loop.
        # Word-boundary check so we do not flag unrelated substrings.
        import re
        self.assertFalse(re.search(r"\bretry\b", executable, re.IGNORECASE),
                         "resolver implements a retry loop")


if __name__ == "__main__":
    unittest.main()
