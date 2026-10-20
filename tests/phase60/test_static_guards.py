"""Phase 60 static guards. The scan set is discovered by docstring marker.

A ``pinn/verification`` module whose docstring starts "Phase 60" is scanned,
and so is every planned Phase 60 file that exists, so a later plan's module
joins the scan as soon as it is created. The rules (60-PATTERNS S1 and S2):

* every ``torch.load`` passes the literal keyword ``weights_only=True``;
* no module names a production-checkpoint, runtime, fallback-normalizer or
  corpus-parsing symbol (docstrings and comments are stripped, string literals
  are kept);
* no module imports the evaluator or the trainer entry point;
* in the ``pinn/verification`` modules, no handler that names ``OwnerRouted``,
  ``CrossCheckDisagreement``, ``Exception`` or ``BaseException`` (or is bare)
  swallows the stop: it ends with a bare ``raise`` or is on the short allowlist;
* the trainer, the evaluator, the training package and the verification
  package initializer import no Phase 60 module.

Every detector is a pure function of source text and has an injected-violation
self-test. The repository-wide scans (sole corpus reader, precision defaults,
v1.3-era references) run in ``tests.phase39.test_prohibitions`` and
``tests.phase38.test_prohibitions``; they are not repeated here.
"""

from __future__ import annotations

import ast
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.phase39.test_prohibitions import executable_source_from_text

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_REL = ".planning/phases/60-single-system-learnability/evidence"

PHASE60_FILES = (
    "pinn/verification/learnability_arms.py",
    "pinn/verification/learnability_data.py",
    "pinn/verification/learnability_losses.py",
    "pinn/verification/learnability_run.py",
    "pinn/verification/learnability_g2.py",
    "pinn/verification/learnability_ruling.py",
    "pinn/verification/learnability_protocol.py",
    "pinn/verification/diagnostic_architecture.py",
    "pinn/verification/gate04_omega_remeasure.py",
    f"{EVIDENCE_REL}/launch_phase60_arm.py",
    f"{EVIDENCE_REL}/verify_phase60_evidence.py",
)

FORBIDDEN_NAMES = frozenset({
    "AdmittedSetAdapter",
    "_build_admitted_sources",
    "TorchSaveCheckpointStore",
    "save_rolling",
    "save_best",
    "save_anchor",
    "build_checkpoint_payload",
    "RunController",
    "CurriculumController",
    "run_stage",
    "PlateauDetector",
    "resolve_runtime",
    "current_fingerprint",
    "runtime_gate",
    "fallback_normalizer_from_allowlist",
    "parse_brutus_file",
    "parse_brutus_text",
    "BRUTUS_FOLDER_TABLE",
})

# Handlers that may name a broad exception without re-raising: a command line
# prints a halt token and returns an exit constant, and the memory-release
# helper wraps a device cache call that frozen rules never reach.
ALLOWED_BROAD_HANDLERS = frozenset({
    ("pinn/verification/learnability_run.py", "main"),
    ("pinn/verification/learnability_g2.py", "main"),
    ("pinn/verification/learnability_protocol.py", "main"),
    ("pinn/verification/gate04_omega_remeasure.py", "main"),
    ("pinn/verification/learnability_losses.py", "release_chunk_memory"),
})
_BROAD_EXCEPTIONS = frozenset({
    "OwnerRouted", "CrossCheckDisagreement", "Exception", "BaseException",
})


# ---------------------------------------------------------------------------
# Discovery.
# ---------------------------------------------------------------------------

def _first_doc_line(path):
    try:
        tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return ""
    doc = ast.get_docstring(tree) or ""
    return doc.splitlines()[0] if doc else ""


def _is_phase60_module(path):
    return _first_doc_line(path).startswith("Phase 60")


def discover_scan_set():
    """Marker-discovered modules unioned with the planned files that exist."""
    pinn = [
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / "pinn" / "verification").glob("*.py"))
        if path.name != "__init__.py" and _is_phase60_module(path)
    ]
    evidence = []
    evidence_root = ROOT / EVIDENCE_REL
    if evidence_root.is_dir():
        evidence = [
            path.relative_to(ROOT).as_posix()
            for path in sorted(evidence_root.rglob("*.py"))
            if "__pycache__" not in path.parts
        ]

    def union(found, prefix):
        planned = [
            item for item in PHASE60_FILES
            if item.startswith(prefix) and (ROOT / item).is_file()
        ]
        return tuple(sorted(set(found) | set(planned)))

    return {
        "pinn": union(pinn, "pinn/verification/"),
        "evidence": union(evidence, EVIDENCE_REL + "/"),
    }


def _existing_sources():
    found = []
    for kind, entries in discover_scan_set().items():
        for relative in entries:
            path = ROOT / relative
            if path.is_file():
                found.append((kind, relative, path.read_text(encoding="utf-8")))
    return found


def _phase60_modules():
    return tuple(
        relative[:-3].replace("/", ".") for relative in discover_scan_set()["pinn"]
    )


# ---------------------------------------------------------------------------
# Detectors (pure functions of source text).
# ---------------------------------------------------------------------------

def _owner_is_torch(owner, torch_names):
    if isinstance(owner, ast.Name):
        return owner.id in torch_names
    return (
        isinstance(owner, ast.Attribute)
        and owner.attr == "serialization"
        and isinstance(owner.value, ast.Name)
        and owner.value.id in torch_names
    )


def _literal_weights_only_true(call):
    return any(
        keyword.arg == "weights_only"
        and isinstance(keyword.value, ast.Constant)
        and keyword.value.value is True
        for keyword in call.keywords
    )


def torch_load_violations(source):
    """Line numbers of ``torch.load`` calls that lack the literal ``weights_only=True``."""
    tree = ast.parse(source)
    torch_names = {"torch"}
    load_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "torch":
                    torch_names.add(alias.asname or "torch")
        elif isinstance(node, ast.ImportFrom) and node.module in ("torch", "torch.serialization"):
            for alias in node.names:
                if alias.name == "load":
                    load_names.add(alias.asname or "load")
    violations = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        is_load = (
            isinstance(func, ast.Attribute)
            and func.attr == "load"
            and _owner_is_torch(func.value, torch_names)
        ) or (isinstance(func, ast.Name) and func.id in load_names)
        if is_load and not _literal_weights_only_true(node):
            violations.append(node.lineno)
    return violations


def forbidden_name_violations(source):
    """Forbidden symbols in executable source (docstrings and comments stripped)."""
    executable = executable_source_from_text(source)
    return sorted(
        name for name in FORBIDDEN_NAMES
        if re.search(rf"\b{re.escape(name)}\b", executable)
    )


def _resolve_module(node, package):
    """Absolute dotted module of an ``ImportFrom``, resolving a relative level."""
    if node.level == 0:
        return node.module or ""
    parts = package.split(".") if package else []
    parts = parts[: len(parts) - (node.level - 1)] if node.level > 1 else parts
    if node.module:
        parts = parts + node.module.split(".")
    return ".".join(parts)


def imported_module_names(source, package=""):
    """Every dotted name an import statement can bring in, absolute."""
    names = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = _resolve_module(node, package)
            if base:
                names.append(base)
                names.extend(f"{base}.{alias.name}" for alias in node.names)
    return names


def _is_evaluator_module(name):
    if name in {"pinn.evaluate", "pinn.train"}:
        return True
    return name.startswith("pinn.evaluate.") or name.startswith("pinn.train.")


def evaluator_import_violations(source, package=""):
    return [name for name in imported_module_names(source, package) if _is_evaluator_module(name)]


def phase60_import_violations(source, modules, package=""):
    """Imports of any named Phase 60 module, absolute or relative."""
    hits = []
    for name in imported_module_names(source, package):
        if any(name == module or name.startswith(module + ".") for module in modules):
            hits.append(name)
    return hits


def _is_broad(handler_type):
    if handler_type is None:
        return True
    if isinstance(handler_type, ast.Name):
        return handler_type.id in _BROAD_EXCEPTIONS
    if isinstance(handler_type, ast.Attribute):
        return handler_type.attr in _BROAD_EXCEPTIONS
    if isinstance(handler_type, ast.Tuple):
        return any(_is_broad(element) for element in handler_type.elts)
    return False


def _ends_with_bare_raise(body):
    return bool(body) and isinstance(body[-1], ast.Raise) and body[-1].exc is None


class _HandlerScan(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.found = []

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)
        self.functions.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ExceptHandler(self, node):
        if _is_broad(node.type) and not _ends_with_bare_raise(node.body):
            function = self.functions[-1] if self.functions else None
            self.found.append((node.lineno, function))
        self.generic_visit(node)


def swallowed_owner_stops(source, relative="<injected>"):
    """Broad handlers that neither end in a bare ``raise`` nor are on the allowlist."""
    scan = _HandlerScan()
    scan.visit(ast.parse(source))
    return [
        (line, function) for line, function in scan.found
        if (relative, function) not in ALLOWED_BROAD_HANDLERS
    ]


def _package_of(relative):
    return ".".join(Path(relative).parent.parts)


# ---------------------------------------------------------------------------
# Real scans.
# ---------------------------------------------------------------------------

class DiscoveryTests(unittest.TestCase):
    def test_scan_set_names_the_plan_60_01_modules(self):
        pinn = discover_scan_set()["pinn"]
        for name in ("arms", "data", "losses", "run"):
            self.assertIn(f"pinn/verification/learnability_{name}.py", pinn)

    def test_every_planned_pinn_path_is_a_verification_module_or_an_evidence_script(self):
        self.assertEqual(len(PHASE60_FILES), 11)
        for item in PHASE60_FILES:
            self.assertTrue(
                item.startswith("pinn/verification/") or item.startswith(EVIDENCE_REL + "/"),
                item,
            )

    def test_only_phase_60_docstrings_are_discovered_by_marker(self):
        with tempfile.TemporaryDirectory(prefix="phase60-marker-") as tmp:
            marked = Path(tmp) / "marked.py"
            marked.write_text('"""Phase 60 (INST-05): a harness module."""\n', encoding="utf-8")
            other_phase = Path(tmp) / "other.py"
            other_phase.write_text('"""Phase 59 (FEAS-01): a scorer."""\n', encoding="utf-8")
            bare = Path(tmp) / "bare.py"
            bare.write_text("x = 1\n", encoding="utf-8")
            broken = Path(tmp) / "broken.py"
            broken.write_text("def (:\n", encoding="utf-8")
            self.assertTrue(_is_phase60_module(marked))
            self.assertFalse(_is_phase60_module(other_phase))
            self.assertFalse(_is_phase60_module(bare))
            self.assertFalse(_is_phase60_module(broken))

    def test_no_phase_59_marked_module_is_in_the_phase_60_scan(self):
        for relative in discover_scan_set()["pinn"]:
            self.assertTrue(_first_doc_line(ROOT / relative).startswith("Phase 60"), relative)


class StaticGuardTests(unittest.TestCase):
    def test_every_torch_load_passes_weights_only_true(self):
        for _kind, relative, source in _existing_sources():
            with self.subTest(file=relative):
                self.assertEqual(torch_load_violations(source), [])

    def test_scanned_files_name_no_forbidden_symbol(self):
        for _kind, relative, source in _existing_sources():
            with self.subTest(file=relative):
                self.assertEqual(forbidden_name_violations(source), [])

    def test_scanned_files_do_not_import_the_evaluator_or_trainer(self):
        for _kind, relative, source in _existing_sources():
            with self.subTest(file=relative):
                self.assertEqual(evaluator_import_violations(source, _package_of(relative)), [])

    def test_fresh_interpreter_does_not_load_the_evaluator_or_trainer(self):
        modules = _phase60_modules()
        code = (
            "import importlib, sys\n"
            f"for module in {list(modules)!r}:\n"
            "    importlib.import_module(module)\n"
            "    for banned in ('pinn.evaluate', 'pinn.train'):\n"
            "        assert banned not in sys.modules, (module, banned)\n"
        )
        completed = subprocess.run(
            [sys.executable, "-B", "-c", code],
            cwd=str(ROOT), capture_output=True, text=True, timeout=300,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_verification_modules_do_not_swallow_owner_stops(self):
        for relative in discover_scan_set()["pinn"]:
            source = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(file=relative):
                self.assertEqual(swallowed_owner_stops(source, relative), [])

    def test_the_broad_handler_allowlist_is_the_documented_five(self):
        self.assertEqual(len(ALLOWED_BROAD_HANDLERS), 5)
        self.assertEqual({function for _path, function in ALLOWED_BROAD_HANDLERS},
                         {"main", "release_chunk_memory"})

    def test_trainer_evaluator_and_training_package_import_no_phase_60_module(self):
        modules = _phase60_modules()
        paths = [ROOT / "pinn" / "train.py", ROOT / "pinn" / "evaluate.py"]
        paths.extend(
            path for path in sorted((ROOT / "pinn" / "training").rglob("*.py"))
            if "__pycache__" not in path.parts
        )
        for path in paths:
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT).as_posix()
            with self.subTest(file=relative):
                hits = phase60_import_violations(
                    path.read_text(encoding="utf-8"), modules, _package_of(relative)
                )
                self.assertEqual(hits, [])

    def test_the_verification_package_initializer_imports_no_phase_60_module(self):
        relative = "pinn/verification/__init__.py"
        hits = phase60_import_violations(
            (ROOT / relative).read_text(encoding="utf-8"), _phase60_modules(),
            _package_of(relative),
        )
        self.assertEqual(hits, [])


# ---------------------------------------------------------------------------
# Self-tests: every detector fires on an injected violation.
# ---------------------------------------------------------------------------

class DetectorSelfTests(unittest.TestCase):
    def test_weights_only_missing_or_false_fires(self):
        missing = "import torch\ndef load_it(path):\n    return torch.load(path)\n"
        disabled = "import torch\ndef load_it(path):\n    return torch.load(path, weights_only=False)\n"
        computed = "import torch\ndef load_it(path, flag):\n    return torch.load(path, weights_only=flag)\n"
        aliased = "import torch as t\ndef load_it(path):\n    return t.load(path)\n"
        bare_name = "from torch import load\ndef load_it(path):\n    return load(path)\n"
        serialization = "import torch\ndef load_it(path):\n    return torch.serialization.load(path)\n"
        for label, source in (
            ("missing", missing), ("False", disabled), ("computed", computed),
            ("aliased", aliased), ("from-import", bare_name), ("serialization", serialization),
        ):
            with self.subTest(case=label):
                self.assertTrue(torch_load_violations(source))

    def test_weights_only_true_and_unrelated_loads_are_clean(self):
        safe = "import torch\ndef load_it(path):\n    return torch.load(path, map_location='cpu', weights_only=True)\n"
        json_load = "import json\ndef load_it(handle):\n    return json.load(handle)\n"
        method = "def load_it(store, path):\n    return store.load(path)\n"
        jit = "import torch\ndef load_it(path):\n    return torch.jit.load(path)\n"
        for label, source in (("safe", safe), ("json", json_load), ("method", method), ("jit", jit)):
            with self.subTest(case=label):
                self.assertEqual(torch_load_violations(source), [])

    def test_every_forbidden_name_fires_in_code(self):
        for name in sorted(FORBIDDEN_NAMES):
            with self.subTest(name=name):
                self.assertEqual(forbidden_name_violations(f"value = {name}()\n"), [name])

    def test_a_forbidden_name_inside_a_string_literal_fires(self):
        self.assertEqual(
            forbidden_name_violations("handle = getattr(module, 'resolve_runtime')\n"),
            ["resolve_runtime"],
        )

    def test_a_forbidden_name_in_a_docstring_or_comment_is_inert(self):
        source = (
            '"""This module never calls resolve_runtime or RunController."""\n'
            "# TorchSaveCheckpointStore is not used here\n"
            "def work():\n"
            '    """Does not use run_stage."""\n'
            "    return 1\n"
        )
        self.assertEqual(forbidden_name_violations(source), [])

    def test_a_longer_identifier_that_contains_a_forbidden_name_is_not_a_hit(self):
        self.assertEqual(forbidden_name_violations("run_stage_count = 3\n"), [])

    def test_evaluator_and_trainer_imports_fire(self):
        for source in (
            "import pinn.evaluate\n",
            "import pinn.train\n",
            "from pinn.train import main\n",
            "from pinn.evaluate import evaluate_run\n",
            "from pinn import evaluate\n",
            "from pinn import train\n",
            "import pinn.train.helpers\n",
        ):
            with self.subTest(source=source):
                self.assertTrue(evaluator_import_violations(source))

    def test_the_training_package_is_not_the_trainer(self):
        for source in (
            "from pinn.training import config\n",
            "import pinn.training.checkpoint\n",
            "from pinn.training.controllers import accumulate_chunked_data_term\n",
        ):
            with self.subTest(source=source):
                self.assertEqual(evaluator_import_violations(source), [])

    def test_a_relative_import_of_the_trainer_fires_inside_its_package(self):
        self.assertTrue(evaluator_import_violations("from . import evaluate\n", "pinn"))
        self.assertTrue(evaluator_import_violations("from .train import main\n", "pinn"))
        self.assertEqual(evaluator_import_violations("from . import config\n", "pinn.training"), [])

    def test_a_swallowed_owner_stop_fires(self):
        for label, source in (
            ("OwnerRouted pass", "def f():\n    try:\n        counts()\n    except OwnerRouted:\n        pass\n"),
            ("OwnerRouted retry", "def f():\n    try:\n        counts()\n    except OwnerRouted:\n        return retry()\n"),
            ("attribute", "def f():\n    try:\n        run()\n    except scorecard.OwnerRouted:\n        pass\n"),
            ("cross-check", "def f():\n    try:\n        run()\n    except CrossCheckDisagreement:\n        pass\n"),
            ("Exception", "def f():\n    try:\n        run()\n    except Exception:\n        return None\n"),
            ("BaseException", "def f():\n    try:\n        run()\n    except BaseException:\n        return None\n"),
            ("bare", "def f():\n    try:\n        run()\n    except:\n        pass\n"),
            ("tuple", "def f():\n    try:\n        run()\n    except (ValueError, OwnerRouted):\n        pass\n"),
            ("wrapped raise", "def f():\n    try:\n        run()\n    except Exception as exc:\n        raise RuntimeError('x') from exc\n"),
            ("raise not last", "def f():\n    try:\n        run()\n    except Exception:\n        raise\n        return 1\n"),
            ("module level", "try:\n    run()\nexcept Exception:\n    pass\n"),
        ):
            with self.subTest(case=label):
                self.assertTrue(swallowed_owner_stops(source))

    def test_a_handler_that_ends_with_a_bare_raise_or_is_narrow_is_clean(self):
        for label, source in (
            ("re-raise", "def f():\n    try:\n        run()\n    except OwnerRouted as exc:\n        log(exc)\n        raise\n"),
            ("broad re-raise", "def f():\n    try:\n        run()\n    except Exception:\n        cleanup()\n        raise\n"),
            ("narrow", "def f():\n    try:\n        run()\n    except KeyError:\n        pass\n"),
            ("narrow tuple", "def f():\n    try:\n        run()\n    except (KeyError, ValueError) as exc:\n        raise Halt('x') from exc\n"),
            ("no handler", "def f():\n    return run()\n"),
        ):
            with self.subTest(case=label):
                self.assertEqual(swallowed_owner_stops(source), [])

    def test_the_allowlist_exempts_only_the_named_function_in_the_named_file(self):
        main = (
            "def main():\n"
            "    try:\n"
            "        run()\n"
            "    except Exception as exc:\n"
            "        print('HALT', exc)\n"
            "        return 2\n"
        )
        release = (
            "def release_chunk_memory(device):\n"
            "    try:\n"
            "        empty_cache()\n"
            "    except Exception:\n"
            "        pass\n"
        )
        self.assertEqual(swallowed_owner_stops(main, "pinn/verification/learnability_run.py"), [])
        self.assertEqual(swallowed_owner_stops(main, "pinn/verification/learnability_g2.py"), [])
        self.assertEqual(
            swallowed_owner_stops(release, "pinn/verification/learnability_losses.py"), []
        )
        self.assertTrue(swallowed_owner_stops(main, "pinn/verification/learnability_data.py"))
        self.assertTrue(swallowed_owner_stops(release, "pinn/verification/learnability_run.py"))
        renamed = main.replace("def main()", "def run_everything()")
        self.assertTrue(swallowed_owner_stops(renamed, "pinn/verification/learnability_run.py"))

    def test_a_training_package_import_of_a_phase_60_module_fires(self):
        modules = (
            "pinn.verification.learnability_run",
            "pinn.verification.learnability_arms",
        )
        for source, package in (
            ("from pinn.verification import learnability_run\n", "pinn.training"),
            ("import pinn.verification.learnability_arms\n", "pinn"),
            ("from pinn.verification.learnability_run import run_arm\n", "pinn.training"),
            ("from pinn.verification.learnability_arms.sub import thing\n", "pinn"),
            ("from . import learnability_run\n", "pinn.verification"),
            ("from .learnability_arms import ArmSpec\n", "pinn.verification"),
            ("from .. import verification\nfrom ..verification import learnability_run\n", "pinn.training"),
        ):
            with self.subTest(source=source):
                self.assertTrue(phase60_import_violations(source, modules, package))

    def test_imports_of_other_verification_modules_are_clean(self):
        modules = ("pinn.verification.learnability_run",)
        for source, package in (
            ("from pinn.verification import evidence_io\n", "pinn.training"),
            ("from . import componentwise_ad\n", "pinn.verification"),
            ("from pinn.verification.learnability_run_extra import thing\n", "pinn"),
            ("import pinn.verification.feasibility_scorer\n", "pinn"),
        ):
            with self.subTest(source=source):
                self.assertEqual(phase60_import_violations(source, modules, package), [])


if __name__ == "__main__":
    unittest.main()
