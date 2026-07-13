"""Contract tests for Phase 38 rung 2, the fp64-CPU residual gradcheck probe."""

from __future__ import annotations

import ast
import importlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = "pinn.verification.gradcheck_probe"
PROBE_PATH = ROOT / "pinn" / "verification" / "gradcheck_probe.py"


def _load_probe():
    """Defer the production import so RED is SKIP rather than an import error."""
    try:
        return importlib.import_module(MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{MODULE} has not landed yet: {exc}") from exc


def _executable_source(path: pathlib.Path) -> str:
    """Return executable Python, excluding docstrings and comments."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    docstring_lines: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc and node.body and isinstance(node.body[0], ast.Expr):
                expr = node.body[0]
                for lineno in range(expr.lineno, (expr.end_lineno or expr.lineno) + 1):
                    docstring_lines.add(lineno)
    return "\n".join(
        line.strip()
        for lineno, line in enumerate(source.splitlines(), start=1)
        if lineno not in docstring_lines and line.strip() and not line.lstrip().startswith("#")
    )


class GradcheckProbeTests(unittest.TestCase):
    """Rung 2 locks explicit arm selection, fp64-CPU PASS, and evidence facts."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="phase38-gradcheck-")
        self.addCleanup(self._tmp.cleanup)
        self.evidence_root = pathlib.Path(self._tmp.name) / "evidence" / "gradcheck"

    def _run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", MODULE, *args, "--evidence-root", str(self.evidence_root)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def _raw_runs(self) -> list[pathlib.Path]:
        return sorted(self.evidence_root.glob("*/raw.json"))

    def test_cli_requires_precision_and_device(self):
        _load_probe()
        missing_precision = self._run_cli("--device", "cpu")
        self.assertNotEqual(missing_precision.returncode, 0)
        missing_device = self._run_cli("--precision", "float64")
        self.assertNotEqual(missing_device.returncode, 0)

    def test_fp64_cpu_gradcheck_passes_and_records_evidence(self):
        _load_probe()
        completed = self._run_cli("--precision", "float64", "--device", "cpu")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("PASS", completed.stdout)
        self.assertIn("eps=1e-06", completed.stdout)
        self.assertIn("atol=1e-05", completed.stdout)
        self.assertIn("rtol=0.001", completed.stdout)

        raw_runs = self._raw_runs()
        self.assertEqual(len(raw_runs), 1)
        run_dir = raw_runs[0].parent
        self.assertTrue((run_dir / "summary.md").is_file())
        raw = json.loads(raw_runs[0].read_text(encoding="utf-8"))
        self.assertEqual(raw["arm"], {"precision": "float64", "device": "cpu"})
        self.assertEqual(raw["tolerances"], {"eps": 1e-6, "atol": 1e-5, "rtol": 1e-3})
        self.assertTrue(raw["gradcheck_result"])
        self.assertIn("pre_import_fallback", raw)
        self.assertIn("torch_build", raw)

    def test_source_has_no_precision_default(self):
        _load_probe()
        executable = _executable_source(PROBE_PATH)
        self.assertIn('add_argument("--precision", required=True', executable)
        self.assertNotIn('add_argument("--precision", default=', executable)
        self.assertNotIn("add_argument('--precision', default=", executable)


if __name__ == "__main__":
    unittest.main()
