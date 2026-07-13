"""Phase 38 / NET-03 — read-only Brutus fixture-loader test contract.

Wave 3 contract (RED-first). Production symbols are imported inside the test
methods via PER-SYMBOL deferred imports, so this suite SKIPs cleanly (never
ERRORs) before ``pinn/verification/fixture_loader.py`` lands, and turns green
at task 38-03-02.

Grounding (``simulation_data/Documentation/README.md`` — File Schemas, File
Naming Conventions, Mandatory Parsing Rules; ``.claude/rules/dataset-reference.md``):

  * IC file  : 3 lines, ``m x y z vx vy vz`` per body.
  * Brutus   : repeating snapshots — header ``t N t_cpu`` then 3 body lines
               ``m x y z vx vy vz``, blank-line separated; an OPTIONAL
               ``Result: ...`` footer whose schema is heterogeneous and which
               must be treated as metadata only.
  * Completeness: final timestamp >= 9.5. Do NOT rely on ``Result:``.
  * Folder defines the variant; the numeric ID (zero-padded to 4) maps IC to
    Brutus output; file names do NOT encode "gold".

Governance: ``simulation_data/`` is STRICTLY READ-ONLY. Every fixture in this
suite is synthesized in a unittest temporary directory — no test touches the
real dataset tree, and the loader is asserted never to open a file for writing
or to create a directory.

Scope (CTX-25..27): this loader is NOT the Phase 39 adapter. It implements no
Step-1A gate, no splits, no batching, and no data_version_hash.
"""

import hashlib
import importlib
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

LOADER_MODULE = "pinn.verification.fixture_loader"

COMPLETENESS_MIN_FINAL_TIME = 9.5


def _load_torch():
    try:
        import torch
    except ImportError as exc:  # pragma: no cover - environment guard
        raise unittest.SkipTest(f"torch not installed: {exc}")
    return torch


def _require_module(module_name=LOADER_MODULE):
    """Deferred module import. SkipTest (never ERROR) if it is not implemented."""
    try:
        return importlib.import_module(module_name)
    except ImportError as exc:
        raise unittest.SkipTest(f"{module_name} not implemented yet: {exc}")


def _require(symbol_name, module_name=LOADER_MODULE):
    """Per-symbol deferred import. SkipTest if the module OR symbol is absent."""
    module = _require_module(module_name)
    if not hasattr(module, symbol_name):
        raise unittest.SkipTest(f"{module_name}.{symbol_name} not implemented yet")
    return getattr(module, symbol_name)


# ---------------------------------------------------------------------------
# Synthetic in-format fixtures (tmp dir only — never under simulation_data/).
# ---------------------------------------------------------------------------

MASSES = (1.3490330328149076, 0.3068019185652623, 1.3441650486198304)


def _body_line(mass, index, t):
    """One body line ``m x y z vx vy vz`` with deterministic, distinct values."""
    x = 1.0 + index + 0.1 * t
    y = -0.5 * (index + 1) + 0.2 * t
    z = 0.05 * (index + 1) - 0.01 * t
    vx = 0.3 * (index + 1)
    vy = -0.2 * (index + 1)
    vz = 0.01 * (index + 1)
    return f"{mass!r} {x!r} {y!r} {z!r} {vx!r} {vy!r} {vz!r}"


def write_brutus_file(path, times, masses=MASSES, footer=None):
    """Write a synthetic Brutus-format trajectory to ``path`` (a tmp path)."""
    lines = []
    for t in times:
        lines.append(f"{t!r} 3 {0.5 * t!r}")
        for i, m in enumerate(masses):
            lines.append(_body_line(m, i, t))
        lines.append("")
    if footer is not None:
        lines.append(footer)
    Path(path).write_text("\n".join(lines) + "\n")
    return Path(path)


def write_ic_file(path, masses=MASSES):
    """Write a synthetic 3-line IC file to ``path`` (a tmp path)."""
    lines = [_body_line(m, i, 0.0) for i, m in enumerate(masses)]
    Path(path).write_text("\n".join(lines) + "\n")
    return Path(path)


def complete_times(n=12):
    """Times whose FINAL value is >= 9.5 (passes the completeness gate)."""
    return [round(i * (10.0 / (n - 1)), 6) for i in range(n)]


def truncated_times(n=6):
    """Times whose FINAL value is < 9.5 (fails the completeness gate)."""
    return [round(i * (4.0 / (n - 1)), 6) for i in range(n)]


class Sha256Tests(unittest.TestCase):
    def test_sha256_file_matches_hashlib(self):
        sha256_file = _require("sha256_file")
        with TemporaryDirectory() as tmp:
            p = Path(tmp) / "brutus_standard_0000.txt"
            write_brutus_file(p, complete_times())
            expected = hashlib.sha256(p.read_bytes()).hexdigest()
            self.assertEqual(sha256_file(p), expected)


class ResolveTrajectoryPathTests(unittest.TestCase):
    """Folder mapping + typed input validation BEFORE any path is constructed."""

    def _resolve(self):
        return _require("resolve_trajectory_path")

    def test_known_variants_map_to_the_documented_folders(self):
        resolve = self._resolve()
        cases = {
            "standard_quasi_random": (
                "brutus_standard_quasi_random", "brutus_standard_0007.txt",
                "ic_standard_quasi_random", "ic_standard_0007.txt"),
            "standard_quasi_random_gold_standard": (
                "brutus_standard_quasi_random_gold_standard",
                "brutus_standard_0007.txt",
                "ic_standard_quasi_random", "ic_standard_0007.txt"),
            "hierarchical": (
                "brutus_hierarchical", "brutus_hierarchical_0007.txt",
                "ic_hierarchical", "ic_hierarchical_0007.txt"),
            "hierarchical_gold_standard": (
                "brutus_hierarchical_gold_standard",
                "brutus_hierarchical_0007.txt",
                "ic_hierarchical", "ic_hierarchical_0007.txt"),
        }
        for variant, (b_dir, b_name, i_dir, i_name) in cases.items():
            resolved = resolve(variant, 7)
            brutus = Path(resolved.brutus_path)
            ic = Path(resolved.ic_path)
            self.assertEqual(brutus.name, b_name, variant)
            self.assertEqual(brutus.parent.name, b_dir, variant)
            self.assertEqual(ic.name, i_name, variant)
            self.assertEqual(ic.parent.name, i_dir, variant)
            self.assertEqual(resolved.variant, variant)
            self.assertEqual(resolved.id, "0007")
            # Gold status is encoded ONLY by the folder — never in the filename.
            self.assertNotIn("gold", brutus.name)

    def test_id_is_zero_padded_to_four_digits(self):
        resolve = self._resolve()
        self.assertEqual(resolve("hierarchical", 0).id, "0000")
        self.assertEqual(resolve("hierarchical", "12").id, "0012")
        self.assertEqual(resolve("hierarchical", 2749).id, "2749")

    def test_unknown_variant_raises_value_error(self):
        resolve = self._resolve()
        for bad in ("standard", "gold", "", "brutus_hierarchical", None):
            with self.assertRaises(ValueError):
                resolve(bad, 1)

    def test_non_numeric_or_out_of_range_id_raises_value_error(self):
        resolve = self._resolve()
        for bad in ("abc", "1.5", "-1", -1, "", None, 10000, "00001"):
            with self.assertRaises(ValueError):
                resolve("hierarchical", bad)

    def test_traversal_ids_are_rejected_before_any_path_is_built(self):
        resolve = self._resolve()
        traversal = [
            "..", "../..", "../../etc/passwd", "0000/../../../etc/passwd",
            "/etc/passwd", "0000/0000", "0000\\0000", "~", "0000%2F..",
        ]
        for bad in traversal:
            with self.assertRaises(ValueError):
                resolve("hierarchical", bad)

    def test_resolved_paths_stay_inside_the_dataset_folders(self):
        resolve = self._resolve()
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "Data"
            resolved = resolve("hierarchical", 3, root=root)
            brutus = Path(resolved.brutus_path).resolve()
            ic = Path(resolved.ic_path).resolve()
            self.assertTrue(str(brutus).startswith(str(root.resolve())))
            self.assertTrue(str(ic).startswith(str(root.resolve())))


class LoadTrajectoryTests(unittest.TestCase):
    """Parse / shapes / dtypes / provenance / completeness on a tmp fixture."""

    def _load(self):
        return _require("load_trajectory")

    def test_parses_shapes_and_dtypes_from_a_path(self):
        torch = _load_torch()
        load_trajectory = self._load()
        times = complete_times(12)
        with TemporaryDirectory() as tmp:
            p = write_brutus_file(Path(tmp) / "brutus_standard_0000.txt", times)
            fixture = load_trajectory(path=p, dtype=torch.float64,
                                      device=torch.device("cpu"))
        n = len(times)
        self.assertEqual(tuple(fixture.times.shape), (n,))
        self.assertEqual(tuple(fixture.positions.shape), (n, 3, 3))
        self.assertEqual(tuple(fixture.velocities.shape), (n, 3, 3))
        self.assertEqual(tuple(fixture.masses.shape), (3,))
        for tensor in (fixture.times, fixture.positions, fixture.velocities,
                       fixture.masses):
            self.assertEqual(tensor.dtype, torch.float64)
            self.assertEqual(tensor.device.type, "cpu")
        self.assertAlmostEqual(float(fixture.times[0]), times[0], places=9)
        self.assertAlmostEqual(float(fixture.times[-1]), times[-1], places=9)
        for i, m in enumerate(MASSES):
            self.assertAlmostEqual(float(fixture.masses[i]), m, places=12)
        # Body 1 x at t = 0 is 1.0 + index + 0.1*t = 2.0 (see _body_line).
        self.assertAlmostEqual(float(fixture.positions[0][1][0]), 2.0, places=9)
        self.assertAlmostEqual(float(fixture.velocities[0][2][0]), 0.9, places=9)

    def test_records_provenance_including_sha256(self):
        torch = _load_torch()
        load_trajectory = self._load()
        with TemporaryDirectory() as tmp:
            p = write_brutus_file(Path(tmp) / "brutus_standard_0000.txt",
                                  complete_times())
            expected = hashlib.sha256(p.read_bytes()).hexdigest()
            fixture = load_trajectory(path=p, dtype=torch.float64,
                                      device=torch.device("cpu"))
        prov = fixture.provenance
        self.assertEqual(prov["sha256"], expected)
        self.assertEqual(Path(prov["path"]).name, "brutus_standard_0000.txt")
        self.assertIn("variant", prov)
        self.assertIn("id", prov)
        self.assertEqual(prov["n_snapshots"], len(complete_times()))
        self.assertGreaterEqual(prov["final_time"], COMPLETENESS_MIN_FINAL_TIME)

    def test_variant_and_id_resolution_records_variant_and_id_provenance(self):
        torch = _load_torch()
        load_trajectory = self._load()
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "Data"
            b_dir = root / "brutus_output" / "brutus_hierarchical_gold_standard"
            i_dir = root / "ic_final" / "ic_hierarchical"
            b_dir.mkdir(parents=True)
            i_dir.mkdir(parents=True)
            brutus = write_brutus_file(b_dir / "brutus_hierarchical_0042.txt",
                                       complete_times())
            write_ic_file(i_dir / "ic_hierarchical_0042.txt")
            fixture = load_trajectory(
                variant="hierarchical_gold_standard", id=42, root=root,
                dtype=torch.float64, device=torch.device("cpu"))
        prov = fixture.provenance
        self.assertEqual(prov["variant"], "hierarchical_gold_standard")
        self.assertEqual(prov["id"], "0042")
        self.assertEqual(Path(prov["path"]).name, brutus.name)
        self.assertEqual(prov["sha256"],
                         hashlib.sha256(brutus.read_bytes()).hexdigest())
        self.assertEqual(Path(prov["ic_path"]).name, "ic_hierarchical_0042.txt")
        for i, m in enumerate(MASSES):
            self.assertAlmostEqual(float(fixture.masses[i]), m, places=12)

    def test_exactly_one_of_path_or_variant_id_is_required(self):
        torch = _load_torch()
        load_trajectory = self._load()
        kw = dict(dtype=torch.float64, device=torch.device("cpu"))
        with self.assertRaises(ValueError):
            load_trajectory(**kw)  # neither
        with TemporaryDirectory() as tmp:
            p = write_brutus_file(Path(tmp) / "brutus_standard_0000.txt",
                                  complete_times())
            with self.assertRaises(ValueError):
                load_trajectory(path=p, variant="hierarchical", id=1, **kw)
            with self.assertRaises(ValueError):
                load_trajectory(variant="hierarchical", **kw)  # id missing
            with self.assertRaises(ValueError):
                load_trajectory(id=1, **kw)  # variant missing

    def test_incomplete_trajectory_is_rejected(self):
        torch = _load_torch()
        load_trajectory = self._load()
        with TemporaryDirectory() as tmp:
            p = write_brutus_file(Path(tmp) / "brutus_standard_0001.txt",
                                  truncated_times())
            with self.assertRaises(ValueError):
                load_trajectory(path=p, dtype=torch.float64,
                                device=torch.device("cpu"))

    def test_result_footer_is_optional_metadata_only(self):
        """All three observed footer schemas parse identically to no footer,
        and a footer claiming t_end >= 9.5 never rescues a truncated file."""
        torch = _load_torch()
        load_trajectory = self._load()
        footers = [
            None,
            ("Result: filename= /x/ic_0000.txt N= 3 t_begin= 0 t_end= 10 dt= 0.08 "
             "eta= 0.263027 tol= 1e-15 Lw= 130 t_cpu= 11.2667 E_initial= -1.23733 "
             "E_final= -1.23733 dE/E= 1.49235e-14"),
            ("Result: filename= /x/ic_0000.txt N= 3 t_begin= 0.0 t_end= 10.0 dt= 0.08 "
             "tol= 1e-15 Lw= 130 t_cpu= 8.5887 E_initial= -3.11082 E_final= -3.11082 "
             "dE/E= 1.97004e-14"),
            ("Result: filename= C:\\x\\ic_0000.txt N= 3 t_begin= 0.0 t_end= 10.01 "
             "dt= 0.01 Lw= 130 t_cpu= 431.969 E_initial= -2.10843 E_final= -2.10843 "
             "dE/E= 1.44300e-12"),
        ]
        shapes = []
        with TemporaryDirectory() as tmp:
            for k, footer in enumerate(footers):
                p = write_brutus_file(Path(tmp) / f"brutus_standard_{k:04d}.txt",
                                      complete_times(), footer=footer)
                fx = load_trajectory(path=p, dtype=torch.float64,
                                     device=torch.device("cpu"))
                shapes.append(tuple(fx.positions.shape))
            self.assertEqual(len(set(shapes)), 1)
            # A footer claiming a complete run does NOT rescue a truncated file.
            bad = write_brutus_file(Path(tmp) / "brutus_standard_0009.txt",
                                    truncated_times(), footer=footers[1])
            with self.assertRaises(ValueError):
                load_trajectory(path=bad, dtype=torch.float64,
                                device=torch.device("cpu"))

    def test_missing_file_raises(self):
        torch = _load_torch()
        load_trajectory = self._load()
        with TemporaryDirectory() as tmp:
            missing = Path(tmp) / "brutus_standard_9999.txt"
            with self.assertRaises((FileNotFoundError, ValueError)):
                load_trajectory(path=missing, dtype=torch.float64,
                                device=torch.device("cpu"))


class ReadOnlyDisciplineTests(unittest.TestCase):
    """The loader NEVER opens a file for writing and NEVER creates a directory.

    ``simulation_data/`` is strictly read-only (project governance); the loader
    is the only Phase 38 module that touches the dataset tree at all.
    """

    def test_loader_opens_only_in_read_mode_and_never_mkdirs(self):
        torch = _load_torch()
        load_trajectory = _require("load_trajectory")
        import builtins

        real_open = builtins.open
        real_mkdir = os.mkdir
        real_makedirs = os.makedirs
        real_path_open = Path.open
        observed_modes = []
        mutations = []

        def spy_open(file, mode="r", *args, **kwargs):
            observed_modes.append(str(mode))
            return real_open(file, mode, *args, **kwargs)

        def spy_path_open(self, mode="r", *args, **kwargs):
            observed_modes.append(str(mode))
            return real_path_open(self, mode, *args, **kwargs)

        def spy_mkdir(*args, **kwargs):
            mutations.append(("mkdir", args))
            return real_mkdir(*args, **kwargs)

        def spy_makedirs(*args, **kwargs):
            mutations.append(("makedirs", args))
            return real_makedirs(*args, **kwargs)

        with TemporaryDirectory() as tmp:
            p = write_brutus_file(Path(tmp) / "brutus_standard_0000.txt",
                                  complete_times())
            builtins.open = spy_open
            Path.open = spy_path_open
            os.mkdir = spy_mkdir
            os.makedirs = spy_makedirs
            try:
                observed_modes.clear()
                load_trajectory(path=p, dtype=torch.float64,
                                device=torch.device("cpu"))
            finally:
                builtins.open = real_open
                Path.open = real_path_open
                os.mkdir = real_mkdir
                os.makedirs = real_makedirs

        self.assertTrue(observed_modes, "loader did not open the fixture at all")
        for mode in observed_modes:
            self.assertNotIn("w", mode)
            self.assertNotIn("a", mode)
            self.assertNotIn("x", mode)
            self.assertNotIn("+", mode)
        self.assertEqual(mutations, [])

    def test_module_source_contains_no_write_mode_or_mkdir(self):
        """Static backstop: the module never spells a write mode or a mkdir."""
        module = _require_module()
        source = Path(module.__file__).read_text()
        # Strip the docstring/comment lines so prose about read-only discipline
        # does not trip the check; inspect executable code only.
        code_lines = [
            line for line in source.splitlines()
            if not line.lstrip().startswith("#")
        ]
        code = "\n".join(code_lines)
        for banned in ("mkdir(", "makedirs(", "write_text(", "write_bytes(",
                       "shutil.", "os.remove", "os.rename"):
            self.assertNotIn(banned, code, f"banned write API {banned!r} present")


class ScopeBoundaryTests(unittest.TestCase):
    """CTX-25..27 — this is NOT the Phase 39 adapter."""

    def test_no_phase39_surface_is_exported(self):
        module = _require_module()
        for forbidden in ("step_1a_gate", "make_splits", "build_batches",
                          "data_version_hash", "DataLoader", "collate"):
            self.assertFalse(hasattr(module, forbidden),
                             f"Phase 39 surface {forbidden!r} leaked into the "
                             f"Phase 38 probe-local loader")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
