"""Phase 59 static guards. The scan set is discovered by glob, tests included."""

from __future__ import annotations

import ast
import re
import subprocess
import sys
import unittest
from pathlib import Path

from tests.phase39.test_prohibitions import (
    executable_source,
    executable_source_from_text,
    parses_corpus,
)


ROOT = Path(__file__).resolve().parents[2]
PHASE_BASE = "805de01418c7181f92c5210cdef4bc11c80afe53"
PINN_TRAIN = "<home>/miniforge3/envs/pinn-train/bin/python"
_SUBJECT = re.compile(r"^[a-z]+\(59(-[0-9]+)?\):")

PHASE59_FILES = (
    "pinn/verification/feasibility_scorecard.py",
    "pinn/verification/feasibility_scorer.py",
    "pinn/verification/split_allowlist.py",
    "pinn/verification/production_reference.py",
    "pinn/verification/evidence_io.py",
    "pinn/verification/stage0_census.py",
    "pinn/verification/dataset_survey.py",
    "pinn/verification/two_kepler.py",
    "pinn/verification/nn_copy.py",
    "pinn/verification/baselines.py",
    ".planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py",
    ".planning/phases/59-read-only-baseline-scorecard/evidence/diag07/diag07_common.py",
    ".planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx01_jx10.py",
    ".planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx02_jx05.py",
)

_FORBIDDEN_NAMES = frozenset({
    "AdmittedSetAdapter",
    "_build_admitted_sources",
    "Optimizer",
    "TorchSaveCheckpointStore",
    "compute_trajectory_gate_metrics",
    "compute_validation_gate",
})
_SAVE_CALLS = frozenset({
    "save", "save_checkpoint", "save_rolling", "save_best", "save_anchor",
})
_BANNED_ROOTS = frozenset({"scipy", "pandas", "sklearn", "pytest", "psutil"})
_ALLOWED_ROOTS = set(sys.stdlib_module_names) | {
    "numpy", "torch", "yaml", "pinn", "__future__",
}


def _first_doc_line(path: Path) -> str:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return ""
    doc = ast.get_docstring(tree) or ""
    return doc.splitlines()[0] if doc else ""


def _is_phase59_module(path: Path) -> bool:
    return _first_doc_line(path).startswith("Phase 59")


def discover_scan_set():
    """Three glob groups, unioned with the planned PHASE59_FILES that exist."""
    pinn = []
    for path in sorted((ROOT / "pinn" / "verification").glob("*.py")):
        if path.name == "__init__.py":
            continue
        if _is_phase59_module(path):
            pinn.append(path.relative_to(ROOT).as_posix())
    evidence = []
    evidence_root = ROOT / ".planning/phases/59-read-only-baseline-scorecard/evidence"
    if evidence_root.is_dir():
        for path in sorted(evidence_root.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            evidence.append(path.relative_to(ROOT).as_posix())
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / "tests" / "phase59").glob("*.py"))
    ]

    def union(found, predicate):
        extra = [
            item for item in PHASE59_FILES
            if predicate(item) and (ROOT / item).is_file()
        ]
        return tuple(sorted(set(found) | set(extra)))

    return {
        "pinn": union(pinn, lambda item: item.startswith("pinn/verification/")),
        "evidence": union(
            evidence,
            lambda item: item.startswith(
                ".planning/phases/59-read-only-baseline-scorecard/evidence/"
            ),
        ),
        "tests": union(tests, lambda item: item.startswith("tests/phase59/")),
    }


def phase59_added_modules():
    """Pinn modules first added by a commit whose subject scope is Phase 59."""
    proc = subprocess.run(
        [
            "git", "log", "--diff-filter=A", "--name-only", "--format=%s",
            f"{PHASE_BASE}..HEAD", "--", "pinn/verification",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    added = []
    subject = None
    for raw in proc.stdout.splitlines():
        line = raw.strip()
        if not line:
            # git prints a blank line between the subject and its paths, and
            # no blank line between the last path and the next subject.
            continue
        if line.startswith("pinn/verification/"):
            if line.endswith(".py") and subject and _SUBJECT.match(subject):
                added.append(line)
            continue
        subject = line
    return tuple(added)


def _existing_sources():
    groups = discover_scan_set()
    found = []
    for kind, entries in groups.items():
        for relative in entries:
            path = ROOT / relative
            if path.is_file():
                found.append((kind, relative, path.read_text(encoding="utf-8")))
    return found


def forbidden_name_violations(source):
    tree = ast.parse(source)
    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in _FORBIDDEN_NAMES:
            violations.append(node.id)
        elif isinstance(node, ast.Attribute) and node.attr in _FORBIDDEN_NAMES:
            violations.append(node.attr)
        elif isinstance(node, ast.Attribute) and node.attr == "optim":
            violations.append("torch.optim")
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            violations.extend(_optim_import(node))
        elif isinstance(node, ast.Call):
            name = _called_name(node.func)
            if name in _SAVE_CALLS:
                violations.append(name)
    return violations


def _called_name(func):
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _optim_import(node):
    found = []
    if isinstance(node, ast.Import):
        modules = [alias.name for alias in node.names]
    else:
        modules = [node.module or ""]
        if (node.module or "") == "torch" and any(alias.name == "optim" for alias in node.names):
            found.append("torch.optim")
    for module in modules:
        if module == "torch.optim" or module.startswith("torch.optim."):
            found.append("torch.optim")
    return found


def _module_names(node):
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    if isinstance(node, ast.ImportFrom) and node.module:
        names = [node.module]
        if node.module == "pinn.verification":
            names.extend(f"pinn.verification.{alias.name}" for alias in node.names)
        if node.module == "pinn":
            names.extend(f"pinn.{alias.name}" for alias in node.names)
        return names
    return []


def evaluator_import_violations(source):
    tree = ast.parse(source)
    violations = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        for name in _module_names(node):
            if _is_evaluator_module(name):
                violations.append(name)
    return violations


def _is_evaluator_module(name):
    if name in {"pinn.evaluate", "pinn.train"}:
        return True
    if name.startswith("pinn.evaluate."):
        return True
    if name.startswith("pinn.train.") and not name.startswith("pinn.training"):
        return True
    return False


def _import_roots(tree, *, top_level_only):
    nodes = tree.body if top_level_only else list(ast.walk(tree))
    roots = []
    for node in nodes:
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.append(alias.name.split(".", 1)[0])
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            roots.append(node.module.split(".", 1)[0])
    return roots


def import_surface_violations(source, *, extra=()):
    tree = ast.parse(source)
    allowed = _ALLOWED_ROOTS | set(extra)
    violations = [
        root for root in _import_roots(tree, top_level_only=True) if root not in allowed
    ]
    violations.extend(
        root for root in _import_roots(tree, top_level_only=False) if root in _BANNED_ROOTS
    )
    return violations


def corpus_token_violation(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if parses_corpus(executable_source(path)):
        return True
    tree = ast.parse(text)
    banned = {"parse_brutus_file", "parse_brutus_text", "BRUTUS_FOLDER_TABLE"}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and banned.intersection(
            alias.name for alias in node.names
        ):
            return True
    return False


def torch_load_violations(source):
    tree = ast.parse(source)
    violations = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != "load":
            continue
        owner = node.func.value
        if not isinstance(owner, ast.Name) or owner.id != "torch":
            continue
        literal_true = any(
            keyword.arg == "weights_only"
            and isinstance(keyword.value, ast.Constant)
            and keyword.value.value is True
            for keyword in node.keywords
        )
        if not literal_true:
            violations.append(getattr(node, "lineno", 0))
    return violations


def survey_import_violations(source, phase_modules):
    tree = ast.parse(source)
    violations = []
    phase_modules = set(phase_modules)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        for name in _module_names(node):
            for module in phase_modules:
                if name == module or name.startswith(module + "."):
                    violations.append(name)
    return violations


def _phase_modules():
    return tuple(
        relative[:-3].replace("/", ".")
        for relative in discover_scan_set()["pinn"]
        if relative.endswith(".py")
    )


def _extra_roots(relative):
    if relative.startswith(
        ".planning/phases/59-read-only-baseline-scorecard/evidence/diag07/"
    ):
        return ("diag07_common",)
    return ()


class DiscoveryTests(unittest.TestCase):
    def test_globs_name_the_scorecard_allowlist_and_this_file(self):
        groups = discover_scan_set()
        self.assertIn("pinn/verification/feasibility_scorecard.py", groups["pinn"])
        self.assertIn("pinn/verification/split_allowlist.py", groups["pinn"])
        self.assertIn("tests/phase59/test_static_guards.py", groups["tests"])
        self.assertEqual(len(PHASE59_FILES), 14)
        self.assertTrue(all(item.startswith("pinn/verification/") for item in groups["pinn"]))
        self.assertTrue(all(item.startswith("tests/phase59/") for item in groups["tests"]))


class UnlistedModuleTests(unittest.TestCase):
    def test_phase59_additions_carry_the_marker_and_join_the_scan(self):
        added = phase59_added_modules()
        self.assertIn("pinn/verification/split_allowlist.py", added)
        groups = discover_scan_set()
        for relative in added:
            path = ROOT / relative
            self.assertTrue(_is_phase59_module(path), relative)
            self.assertIn(relative, groups["pinn"], relative)


class ForbiddenNameTests(unittest.TestCase):
    def test_scanned_files_do_not_reference_banned_names_or_checkpoint_writes(self):
        for _kind, relative, source in _existing_sources():
            self.assertEqual(forbidden_name_violations(source), [], relative)


class EvaluatorImportTests(unittest.TestCase):
    def test_scanned_files_do_not_import_the_evaluator_or_trainer(self):
        for _kind, relative, source in _existing_sources():
            self.assertEqual(evaluator_import_violations(source), [], relative)

    def test_fresh_interpreter_does_not_load_the_evaluator(self):
        for module in _phase_modules():
            code = (
                "import importlib, sys\n"
                f"importlib.import_module({module!r})\n"
                "assert 'pinn.evaluate' not in sys.modules\n"
                "assert 'pinn.train' not in sys.modules\n"
            )
            proc = subprocess.run(
                [PINN_TRAIN, "-B", "-c", code],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=180,
            )
            self.assertEqual(proc.returncode, 0, f"{module}\n{proc.stderr}")


class ImportSurfaceTests(unittest.TestCase):
    def test_import_roots_stay_inside_the_allowed_surface(self):
        for kind, relative, source in _existing_sources():
            extra = set(_extra_roots(relative))
            if kind == "tests":
                extra.add("tests")
            self.assertEqual(
                import_surface_violations(source, extra=extra), [], relative
            )


class CorpusTokenTests(unittest.TestCase):
    def test_only_the_allowlist_module_names_corpus_seams(self):
        groups = discover_scan_set()
        offenders = []
        for kind in ("pinn", "evidence"):
            for relative in groups[kind]:
                path = ROOT / relative
                if not path.is_file():
                    continue
                if corpus_token_violation(path) and not relative.endswith(
                    "pinn/verification/split_allowlist.py"
                ):
                    offenders.append(relative)
        self.assertEqual(offenders, [])
        allowlist = ROOT / "pinn/verification/split_allowlist.py"
        self.assertTrue(corpus_token_violation(allowlist))


class TorchLoadTests(unittest.TestCase):
    def test_every_torch_load_passes_weights_only_true(self):
        for _kind, relative, source in _existing_sources():
            self.assertEqual(torch_load_violations(source), [], relative)


class SurveyNonGatingTests(unittest.TestCase):
    def test_training_and_evaluation_do_not_import_phase59_modules(self):
        modules = _phase_modules()
        paths = list((ROOT / "pinn" / "training").rglob("*.py"))
        paths.extend([ROOT / "pinn" / "train.py", ROOT / "pinn" / "evaluate.py"])
        offenders = []
        for path in paths:
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            hits = survey_import_violations(path.read_text(encoding="utf-8"), modules)
            if hits:
                offenders.append((path.relative_to(ROOT).as_posix(), hits))
        self.assertEqual(offenders, [])


class DetectorSelfTests(unittest.TestCase):
    def test_forbidden_names_and_checkpoint_writes_fire_on_injected_source(self):
        adapter = "def test_case():\n    return AdmittedSetAdapter()\n"
        builder = "def test_case():\n    return _build_admitted_sources(None)\n"
        optim = "import torch.optim\n"
        save = "def run(store):\n    store.save_checkpoint(1)\n"
        clean = (
            "def test_case():\n"
            "    return 'AdmittedSetAdapter'\n"
            "class Store:\n"
            "    def save_checkpoint(self, value):\n"
            "        return value\n"
        )
        self.assertTrue(forbidden_name_violations(adapter))
        self.assertTrue(forbidden_name_violations(builder))
        self.assertTrue(forbidden_name_violations(optim))
        self.assertTrue(forbidden_name_violations(save))
        self.assertEqual(forbidden_name_violations(clean), [])

    def test_evaluator_import_detector_ignores_the_training_package(self):
        self.assertTrue(evaluator_import_violations("import pinn.evaluate\n"))
        self.assertTrue(evaluator_import_violations("import pinn.train\n"))
        self.assertTrue(evaluator_import_violations("from pinn import evaluate, train\n"))
        self.assertEqual(
            evaluator_import_violations("from pinn.training import config\n"), []
        )

    def test_import_surface_rejects_foreign_roots_and_accepts_pinn(self):
        self.assertTrue(import_surface_violations("import scipy\n"))
        self.assertTrue(import_surface_violations("import pandas\n"))
        self.assertEqual(
            import_surface_violations("import numpy\nfrom pinn.constants import T_CHARACTERISTIC_TIME\n"),
            [],
        )
        self.assertEqual(
            import_surface_violations("import tests.phase59\n", extra=("tests",)), []
        )

    def test_corpus_token_detector_sees_a_parse_import_and_a_folder_token(self):
        imported = "from pinn.data.adapter import parse_brutus_file\n"
        token = "folder = 'brutus_hierarchical'\n"
        clean = "from pinn.data.preprocessing import preprocess_trajectory\n"
        self.assertTrue(parses_corpus(executable_source_from_text(token)) or _import_has_parse(imported))
        self.assertTrue(_import_has_parse(imported))
        self.assertFalse(parses_corpus(executable_source_from_text(clean)))
        self.assertFalse(_import_has_parse(clean))

    def test_torch_load_requires_a_literal_weights_only_true(self):
        bare = "import torch\ndef run(path):\n    return torch.load(path)\n"
        safe = "import torch\ndef run(path):\n    return torch.load(path, map_location='cpu', weights_only=True)\n"
        self.assertTrue(torch_load_violations(bare))
        self.assertEqual(torch_load_violations(safe), [])

    def test_survey_detector_flags_only_a_phase59_import(self):
        modules = ("pinn.verification.split_allowlist",)
        bad = "from pinn.verification import split_allowlist\n"
        clean = "from pinn.data import types\n"
        self.assertTrue(survey_import_violations(bad, modules))
        self.assertEqual(survey_import_violations(clean, modules), [])


def _import_has_parse(source):
    tree = ast.parse(source)
    banned = {"parse_brutus_file", "parse_brutus_text", "BRUTUS_FOLDER_TABLE"}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and banned.intersection(
            alias.name for alias in node.names
        ):
            return True
    return False


if __name__ == "__main__":
    unittest.main()
