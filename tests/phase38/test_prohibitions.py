"""Phase-wide mechanical prohibition checks for Phase 38 (CTX-32 / SCOPE-18).

Four checks:
  1. Framework-spec byte-identity (endpoint sha256 vs pre-phase committed
     baseline) AND history-aware ``git log --name-only`` empty over both specs.
  2. Write spy: no write/mkdir targets under ``simulation_data/``.
  3. AST: no precision default / set_default_dtype / is_available outside
     ``resolve_runtime`` (glob-discovered Phase-38 modules).
  4. AST: no v1.3-era imports (same module set).

Baseline regeneration (document for operators)::

    PHASE_BASE=9160a5200df5e515998e235eb13a31c664b67057  # phase-38 planning base
    git show ${PHASE_BASE}:pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md | shasum -a 256
    git show ${PHASE_BASE}:pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md | shasum -a 256
    git log --name-only ${PHASE_BASE}..HEAD -- \\
      pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md \\
      pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
"""

from __future__ import annotations

import ast
import builtins
import hashlib
import os
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[2]

# Pre-phase committed baseline (phase-38 planning base commit).
# Regenerated via: git show <PHASE_BASE>:<spec> | shasum -a 256
PHASE_BASE_REF = "9160a5200df5e515998e235eb13a31c664b67057"
SPEC_PATHS = (
    "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md",
    "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md",
)
# Endpoint digests at PHASE_BASE_REF (and still current on milestone/v2.0).
SPEC_BASELINE_SHA256 = {
    SPEC_PATHS[0]: "0b73ba0345d19c1c2ba544913ecd6680dab442790725de7a8fe52903085b9d68",
    SPEC_PATHS[1]: "e629b2fc444317f71cba0fc9e7e9ba75bf18981fc235b9ba4d25acfe681b6dbd",
}

# Known Phase-38 modules that the glob-discovered set must cover (superset).
KNOWN_PHASE38_MODULES = {
    "pinn/constants.py",
    "pinn/architecture_spec.py",
    "pinn/network.py",
    "pinn/com_projection.py",
    "pinn/physics_residual.py",
    "pinn/loss_catalog.py",
    "pinn/verification/fixture_loader.py",
    "pinn/verification/gradcheck_probe.py",
    "pinn/verification/residual_probe.py",
    "pinn/verification/overfit_probe.py",
}

# Glob exclude list: v1.3-era banned files + Phase-37 substrate already covered
# by tests/phase37 and legitimately owning the precision seam.
_EXCLUDE_SUFFIXES = (
    "pinn/basic_architecture.py",
    "pinn/data-processing-pipeline-full.py",
    "pinn/runtime.py",
    "pinn/verification/componentwise_ad.py",
)


def _sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _executable_source(path: pathlib.Path) -> str:
    """Return executable Python text excluding docstrings and comments."""
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


def _discover_phase38_modules() -> list[pathlib.Path]:
    """Glob ``pinn/**/*.py`` minus the documented exclude list."""
    discovered: list[pathlib.Path] = []
    for path in sorted((ROOT / "pinn").rglob("*.py")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.endswith("__init__.py"):
            continue
        if "data-handling" in rel.split("/"):
            continue
        if rel in _EXCLUDE_SUFFIXES:
            continue
        if any(rel.endswith(ex.split("/")[-1]) and ex in rel for ex in _EXCLUDE_SUFFIXES):
            # Match by full relative path membership.
            if rel in _EXCLUDE_SUFFIXES:
                continue
        if rel in {
            "pinn/basic_architecture.py",
            "pinn/data-processing-pipeline-full.py",
            "pinn/runtime.py",
            "pinn/verification/componentwise_ad.py",
        }:
            continue
        discovered.append(path)
    return discovered


class ProhibitionTests(unittest.TestCase):
    """Mechanical phase-wide prohibition checks."""

    def test_spec_byte_identity_endpoint_sha256(self):
        for rel, expected in SPEC_BASELINE_SHA256.items():
            path = ROOT / rel
            self.assertTrue(path.is_file(), f"missing spec {rel}")
            got = _sha256_file(path)
            self.assertEqual(
                got, expected,
                f"working-tree {rel} sha256 {got} != pre-phase baseline {expected}; "
                f"SCOPE-18 prohibits Phase-38 edits to framework specs",
            )

    def test_spec_history_no_touch_since_phase_base(self):
        completed = subprocess.run(
            [
                "git", "log", "--name-only", "--pretty=format:",
                f"{PHASE_BASE_REF}..HEAD", "--", *SPEC_PATHS,
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        touched = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
        self.assertEqual(
            touched, [],
            f"history-aware check: Phase 38 range touched framework specs: {touched}",
        )

    def test_write_spy_no_simulation_data_writes(self):
        """Run loader + probes under a write spy; none target simulation_data/."""
        from tests.phase38.test_overfit_probe import _write_synthetic_brutus
        from pinn.verification import fixture_loader, gradcheck_probe, residual_probe, overfit_probe

        dataset_root = (ROOT / "simulation_data").resolve()
        write_hits: list[str] = []

        def _check_target(target):
            try:
                resolved = pathlib.Path(target).resolve()
            except (TypeError, ValueError, OSError):
                return
            try:
                resolved.relative_to(dataset_root)
            except ValueError:
                return
            write_hits.append(str(resolved))

        real_open = builtins.open
        real_os_open = os.open
        real_mkdir = os.mkdir
        real_makedirs = os.makedirs
        real_rename = os.rename
        real_replace = os.replace
        real_remove = os.remove

        def spy_open(file, mode="r", *args, **kwargs):
            mode_s = str(mode)
            if any(flag in mode_s for flag in ("w", "a", "x", "+")):
                _check_target(file)
            return real_open(file, mode, *args, **kwargs)

        def spy_os_open(path, flags, *args, **kwargs):
            if flags & (os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC):
                _check_target(path)
            return real_os_open(path, flags, *args, **kwargs)

        def spy_mkdir(path, *args, **kwargs):
            _check_target(path)
            return real_mkdir(path, *args, **kwargs)

        def spy_makedirs(path, *args, **kwargs):
            _check_target(path)
            return real_makedirs(path, *args, **kwargs)

        def spy_rename(src, dst, *args, **kwargs):
            _check_target(dst)
            return real_rename(src, dst, *args, **kwargs)

        def spy_replace(src, dst, *args, **kwargs):
            _check_target(dst)
            return real_replace(src, dst, *args, **kwargs)

        def spy_remove(path, *args, **kwargs):
            _check_target(path)
            return real_remove(path, *args, **kwargs)

        # pathlib Path methods
        real_path_open = pathlib.Path.open
        real_write_text = pathlib.Path.write_text
        real_write_bytes = pathlib.Path.write_bytes
        real_path_mkdir = pathlib.Path.mkdir

        def spy_path_open(self, mode="r", *args, **kwargs):
            mode_s = str(mode)
            if any(flag in mode_s for flag in ("w", "a", "x", "+")):
                _check_target(self)
            return real_path_open(self, mode, *args, **kwargs)

        def spy_write_text(self, *args, **kwargs):
            _check_target(self)
            return real_write_text(self, *args, **kwargs)

        def spy_write_bytes(self, *args, **kwargs):
            _check_target(self)
            return real_write_bytes(self, *args, **kwargs)

        def spy_path_mkdir(self, *args, **kwargs):
            _check_target(self)
            return real_path_mkdir(self, *args, **kwargs)

        with tempfile.TemporaryDirectory(prefix="phase38-prohibition-") as tmp:
            tmp_path = pathlib.Path(tmp)
            fixture = _write_synthetic_brutus(tmp_path / "brutus_0000.txt")
            evidence = tmp_path / "evidence"

            with mock.patch("builtins.open", spy_open), \
                 mock.patch("os.open", spy_os_open), \
                 mock.patch("os.mkdir", spy_mkdir), \
                 mock.patch("os.makedirs", spy_makedirs), \
                 mock.patch("os.rename", spy_rename), \
                 mock.patch("os.replace", spy_replace), \
                 mock.patch("os.remove", spy_remove), \
                 mock.patch.object(pathlib.Path, "open", spy_path_open), \
                 mock.patch.object(pathlib.Path, "write_text", spy_write_text), \
                 mock.patch.object(pathlib.Path, "write_bytes", spy_write_bytes), \
                 mock.patch.object(pathlib.Path, "mkdir", spy_path_mkdir):
                # Loader (read-only).
                fixture_loader.load_trajectory(
                    path=fixture, dtype=__import__("torch").float64,
                    device=__import__("torch").device("cpu"),
                )
                # Gradcheck probe (no trajectory).
                gradcheck_probe.main([
                    "--precision", "float64", "--device", "cpu",
                    "--evidence-root", str(evidence / "gradcheck"),
                ])
                # Residual probe.
                residual_probe.main([
                    "--precision", "float64", "--device", "cpu",
                    "--path", str(fixture),
                    "--evidence-root", str(evidence / "residual"),
                ])
                # Overfit probe (short cap — only need I/O path exercise).
                overfit_probe.main([
                    "--precision", "float64", "--device", "cpu",
                    "--path", str(fixture),
                    "--evidence-root", str(evidence / "overfit"),
                    "--max-steps", "1",
                ])

        self.assertEqual(
            write_hits, [],
            f"write spy observed simulation_data targets: {write_hits}",
        )

    def test_discovered_modules_superset_of_known_phase38(self):
        discovered = {p.relative_to(ROOT).as_posix() for p in _discover_phase38_modules()}
        missing = KNOWN_PHASE38_MODULES - discovered
        self.assertEqual(missing, set(), f"known Phase-38 modules missing from glob set: {missing}")

    def test_no_precision_default_in_discovered_modules(self):
        for path in _discover_phase38_modules():
            with self.subTest(module=path.relative_to(ROOT).as_posix()):
                executable = _executable_source(path)
                self.assertNotIn(
                    "set_default_dtype", executable,
                    f"{path} mutates global default dtype",
                )
                self.assertNotIn(
                    "is_available", executable,
                    f"{path} probes device availability",
                )
                # No argparse precision default (required=True is fine).
                self.assertNotIn('add_argument("--precision", default=', executable)
                self.assertNotIn("add_argument('--precision', default=", executable)

    def test_no_v1_3_era_imports_in_discovered_modules(self):
        banned_tokens = (
            "basic_architecture",
            "data-processing-pipeline-full",
            "data_processing_pipeline_full",
            "data-handling",
            "data_handling",
        )
        for path in _discover_phase38_modules():
            with self.subTest(module=path.relative_to(ROOT).as_posix()):
                executable = _executable_source(path)
                for token in banned_tokens:
                    self.assertNotIn(
                        token, executable,
                        f"{path} appears to import/reference banned v1.3 module {token!r}",
                    )


if __name__ == "__main__":
    unittest.main()
