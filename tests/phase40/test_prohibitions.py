"""Phase 40 mechanical boundary audit (Wave 0) — runs GREEN before production.

Two responsibilities:

1. **Real scans over the CURRENT ``pinn/training/`` tree.** The v1.3-import ban,
   global-default mutation ban, device-availability-probe ban, and
   ``simulation_data`` corpus-path ban are evaluated over the discovered
   ``pinn/training/*.py`` set today. They pass now because the only module
   present is the side-effect-free ``__init__.py``. Discovery is filesystem-driven
   (non-recursive ``glob``), so modules landed by later plans are audited
   automatically WITHOUT editing this file.

2. **Self-verification of every detector.** Because production modules do not
   exist at Wave 1, each mechanical check is additionally proven against a
   SYNTHETIC violating source, so the gate is demonstrably able to FAIL on an
   injected v1 import, global-default mutation, availability probe, corpus-path
   access, or a second-mechanism non-finite contract drift.

The ``NonFiniteContractTests`` class is the SINGLE binding, executable encoding
of the M1 non-finite contract that spans plan 40-02 (producer:
``GradClipper.clip``) and plan 40-05 (consumer: ``RunController``). Both plans
describe the contract in prose, but this class is the only place a violation
becomes a FAILURE — without it, a defensive ``raise`` added in ``grad_clip.py``
or a defensive ``try/except`` added in ``controllers.py`` would satisfy every
other test in the phase while silently creating the second mechanism the
contract forbids.

Grounding: ``tests/phase39/test_prohibitions.py`` (DetectorSelfTests discipline,
the named-module ``.is_file()``-guarded scoped-audit precedent), GAP-40-01/02
(M1 non-finite contract), 40-02-PLAN.md / 40-05-PLAN.md (producer/consumer
halves).
"""

from __future__ import annotations

import ast
import glob
import importlib
import pathlib
import re
import unittest

from tests.phase40 import _SKIP_PHRASE

ROOT = pathlib.Path(__file__).resolve().parents[2]

_LEGACY = {
    "pinn/basic_architecture.py",
    "pinn/data-processing-pipeline-full.py",
}

_V1_TOKENS = ("data-handling", "data_handling", "data-processing-pipeline-full",
              "data_processing_pipeline_full", "basic_architecture")
_GLOBAL_DEFAULT_TOKENS = ("set_default_dtype",)
_CORPUS_PATH_TOKENS = ("simulation_data",)


def _require(symbol, module):
    """Per-symbol deferred import — SkipTest (never ERROR) until it lands."""
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


# ---------------------------------------------------------------------------
# Source extraction (verbatim from tests/phase39/test_prohibitions.py).
# ---------------------------------------------------------------------------

def executable_source_from_text(text, filename="<synthetic>"):
    """Return executable Python text, docstrings and comments stripped."""
    tree = ast.parse(text, filename=filename)
    doc_lines: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc and node.body and isinstance(node.body[0], ast.Expr):
                expr = node.body[0]
                for ln in range(expr.lineno, (expr.end_lineno or expr.lineno) + 1):
                    doc_lines.add(ln)
    return "\n".join(
        line.strip()
        for ln, line in enumerate(text.splitlines(), start=1)
        if ln not in doc_lines and line.strip() and not line.lstrip().startswith("#")
    )


def executable_source(path):
    return executable_source_from_text(pathlib.Path(path).read_text(encoding="utf-8"), str(path))


# ---------------------------------------------------------------------------
# Pure mechanical detectors (each is self-tested below).
# ---------------------------------------------------------------------------

def has_v1_import(exec_src):
    """CTX-17: banned v1.3-era module references."""
    return any(tok in exec_src for tok in _V1_TOKENS)


def has_global_default_mutation(exec_src):
    """No mutation of global torch defaults (precision/device only via resolve_runtime)."""
    return any(tok in exec_src for tok in _GLOBAL_DEFAULT_TOKENS)


def has_availability_probe(exec_src):
    """No ``.is_available()`` device probes (catches cuda/mps/torch.backends.*).

    Matched as a CALL FORM (``.is_available(``) so a legitimately-named
    attribute cannot false-positive.
    """
    return bool(re.search(r"\.is_available\(", exec_src))


def parses_simulation_data(exec_src):
    """No direct ``simulation_data`` corpus-path access."""
    return any(tok in exec_src for tok in _CORPUS_PATH_TOKENS)


def _base_name(node):
    """Return the rightmost attribute/name of a class base, or None."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _is_exception_like(name):
    if not name:
        return False
    return any(name.endswith(suffix) for suffix in ("Error", "Exception", "Fail"))


def defines_or_imports_exception(source_text):
    """AST over RAW text: True if the module OWNS or IMPORTS an exception type.

    A bespoke non-finite mechanism would require the module to define or import
    its own exception type; a bare ``raise ValueError(...)`` on a builtin stays
    legal (construction-time fail-closed validation). Applied to
    ``pinn/training/grad_clip.py`` only, ``.is_file()``-guarded.
    """
    tree = ast.parse(source_text)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if _is_exception_like(_base_name(base)):
                    return True
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for name_pair in node.names:
                bound = name_pair.asname or name_pair.name
                if _is_exception_like(bound):
                    return True
    return False


def has_nonfinite_raise_flag(exec_src):
    """Regex over docstring/comment-stripped source: ``error_if_nonfinite=True``.

    The non-finite signal is the ``GradClipOutcome.non_finite`` flag RETURNED by
    ``GradClipper.clip``; the clipper never passes ``error_if_nonfinite=True``
    (which would turn the measure call into a raising call). Applied to EVERY
    discovered training module.
    """
    return bool(re.search(r"error_if_nonfinite\s*=\s*True", exec_src))


def _contains_clip_call(node):
    """True if ``node``'s subtree contains a ``.clip(...)`` attribute call."""
    for child in ast.walk(node):
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
            if child.func.attr == "clip":
                return True
    return False


def catches_around_clip(source_text):
    """AST over RAW text: True if a handler-bearing ``try`` contains a ``.clip`` call.

    Scoping to ``Try`` nodes with a NON-EMPTY ``handlers`` list is load-bearing:
    40-05 REQUIRES a bare ``try/finally`` (no handlers) to restore
    ``model.train()`` after the validation pass, and a blanket ban on ``Try``
    nodes would collide with it. A handler-less ``try/finally`` cannot swallow a
    signal — only an ``except`` can — so this detector bans exactly the contract
    violation and nothing else. Applied to ``pinn/training/controllers.py`` only,
    ``.is_file()``-guarded.
    """
    tree = ast.parse(source_text)
    for node in ast.walk(tree):
        if isinstance(node, ast.Try) and node.handlers:
            if _contains_clip_call(node):
                return True
    return False


# ---------------------------------------------------------------------------
# Discovery: non-recursive glob of pinn/training/*.py (flat package).
# ---------------------------------------------------------------------------

def discover_training_modules():
    """Filesystem-driven discovery — no hardcoded module-name list.

    Later plans add modules under ``pinn/training/``; this glob picks them up
    automatically so the audit never needs editing per module.
    """
    training_dir = ROOT / "pinn" / "training"
    if not training_dir.is_dir():
        return []
    out = []
    for path in sorted(training_dir.glob("*.py")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.endswith("__init__.py") or rel in _LEGACY:
            continue
        out.append(path)
    return out


# ===========================================================================
# Real scans over the current pinn/training tree.
# ===========================================================================

class TrainingProhibitionsAuditTests(unittest.TestCase):
    """Bans over ``pinn/training/*.py`` (vacuous now; strict as modules land)."""

    def test_no_v1_import_in_training_modules(self):
        for path in discover_training_modules():
            self.assertFalse(has_v1_import(executable_source(path)),
                             f"{path} references a banned v1.3-era module")

    def test_no_global_default_mutation_in_training_modules(self):
        for path in discover_training_modules():
            self.assertFalse(has_global_default_mutation(executable_source(path)),
                             f"{path} mutates a global torch/device default")

    def test_no_availability_probe_in_training_modules(self):
        for path in discover_training_modules():
            self.assertFalse(has_availability_probe(executable_source(path)),
                             f"{path} probes device availability (.is_available())")

    def test_no_simulation_data_access_in_training_modules(self):
        for path in discover_training_modules():
            self.assertFalse(parses_simulation_data(executable_source(path)),
                             f"{path} accesses the simulation_data corpus path directly")

    def test_discovery_is_non_recursive_glob(self):
        # Sanity: the discovered set is a subset of the flat package dir.
        for path in discover_training_modules():
            rel = path.relative_to(ROOT).as_posix()
            self.assertTrue(rel.startswith("pinn/training/"),
                            f"discovery leaked outside pinn/training/: {rel}")


# ===========================================================================
# M1 single-mechanism non-finite contract (40-02 producer + 40-05 consumer).
# ===========================================================================

class NonFiniteContractTests(unittest.TestCase):
    """The SINGLE binding encoding of the M1 non-finite contract.

    Contract (stated ONCE): the non-finite-gradient signal is the
    ``GradClipOutcome.non_finite`` flag RETURNED by ``GradClipper.clip``; the
    clipper never raises, and ``RunController`` branches on the flag and never
    wraps the call in ``try/except``. Both 40-02 and 40-05 describe this in
    prose; this class is the only place a violation becomes a FAILURE.

    The named-module halves are ``.is_file()``-guarded, so they are vacuous at
    Wave 1 (``pinn/training`` empty) and arm themselves automatically the moment
    ``grad_clip.py`` (40-02) and ``controllers.py`` (40-05) land — no edit to
    this file. 40-02 and 40-05 both re-run ``test_prohibitions`` in every verify
    command, so enforcement needs no duplicate check in theirs.
    """

    def test_grad_clip_defines_no_exception_type(self):
        path = ROOT / "pinn" / "training" / "grad_clip.py"
        if path.is_file():
            self.assertFalse(defines_or_imports_exception(path.read_text(encoding="utf-8")),
                             "grad_clip.py defines or imports an exception type "
                             "(the non-finite signal is the returned flag, never a raise)")

    def test_no_module_passes_error_if_nonfinite_true(self):
        for path in discover_training_modules():
            self.assertFalse(has_nonfinite_raise_flag(executable_source(path)),
                             f"{path} passes error_if_nonfinite=True "
                             "(the clipper returns the flag; it never raises)")

    def test_controllers_does_not_catch_around_clip(self):
        path = ROOT / "pinn" / "training" / "controllers.py"
        if path.is_file():
            self.assertFalse(catches_around_clip(path.read_text(encoding="utf-8")),
                             "controllers.py wraps a GradClipper.clip call in try/except "
                             "(RunController branches on the returned flag)")


# ===========================================================================
# Self-verification: every detector must FAIL on an injected violation.
# ===========================================================================

class DetectorSelfTests(unittest.TestCase):
    def test_executable_source_strips_docstrings_and_comments(self):
        src = executable_source_from_text(
            '"""error_if_nonfinite=True in a docstring is inert."""\n'
            "# set_default_dtype in a comment is inert\n"
            "x = 1\n")
        self.assertNotIn("error_if_nonfinite", src)
        self.assertNotIn("set_default_dtype", src)
        self.assertIn("x = 1", src)

    def test_v1_import_detected(self):
        self.assertTrue(has_v1_import("from pinn.basic_architecture import build_network"))
        self.assertTrue(has_v1_import("import data_processing_pipeline_full"))
        self.assertTrue(has_v1_import("from pinn.data_handling.core import parsing"))
        self.assertFalse(has_v1_import("from pinn.data.types import RecordKey"))

    def test_global_default_mutation_detected(self):
        self.assertTrue(has_global_default_mutation("torch.set_default_dtype(torch.float32)"))
        self.assertFalse(has_global_default_mutation("tensor.to(dtype=dtype, device=device)"))

    def test_availability_probe_detected(self):
        self.assertTrue(has_availability_probe("torch.cuda.is_available()"))
        self.assertTrue(has_availability_probe("torch.backends.mps.is_available()"))
        # A legitimately-named attribute is NOT a false positive (call-form match).
        self.assertFalse(has_availability_probe("self.is_available = True"))
        self.assertFalse(has_availability_probe("obj.is_available"))

    def test_simulation_data_access_detected(self):
        self.assertTrue(parses_simulation_data('root = simulation_data_root()'))
        self.assertTrue(parses_simulation_data('path = "simulation_data/brutus_output"'))
        self.assertFalse(parses_simulation_data("from pinn.data.types import RecordKey"))

    def test_defines_or_imports_exception_detected(self):
        # Module OWNS an exception type → True.
        self.assertTrue(defines_or_imports_exception("class OverfitFail(Exception):\n    pass"))
        self.assertTrue(defines_or_imports_exception("class GradClipError(ValueError):\n    pass"))
        # Module IMPORTS an exception type → True.
        self.assertTrue(defines_or_imports_exception("from .errors import OverfitFail"))
        self.assertTrue(defines_or_imports_exception("import some_module.Fail"))
        # Builtin raise (fail-closed validation) → False.
        self.assertFalse(defines_or_imports_exception("raise ValueError('bad quota')"))
        self.assertFalse(defines_or_imports_exception("if x:\n    raise TypeError"))
        # Innocent class / import → False.
        self.assertFalse(defines_or_imports_exception("class RunController:\n    pass"))
        self.assertFalse(defines_or_imports_exception("from pinn.data.types import RecordKey"))

    def test_nonfinite_raise_flag_detected(self):
        # The banned spelling (whitespace-tolerant).
        self.assertTrue(has_nonfinite_raise_flag("measure(x, error_if_nonfinite=True)"))
        self.assertTrue(has_nonfinite_raise_flag("measure(x, error_if_nonfinite = True)"))
        # The legitimate spelling the clipper passes.
        self.assertFalse(has_nonfinite_raise_flag("measure(x, error_if_nonfinite=False)"))
        # Inside a docstring → stripped by executable_source → False (prose immunity).
        self.assertFalse(has_nonfinite_raise_flag(executable_source_from_text(
            '"""error_if_nonfinite=True documents the ban."""\nx = 1')))

    def test_catches_around_clip_detected(self):
        # Handler-bearing try around a .clip call → True (the contract violation).
        self.assertTrue(catches_around_clip(
            "try:\n    clipper.clip(grad)\nexcept Exception:\n    pass"))
        self.assertTrue(catches_around_clip(
            "try:\n    result = self.clipper.clip(g)\nexcept ValueError:\n    result = None"))
        # Bare clip call, no try → False.
        self.assertFalse(catches_around_clip("outcome = clipper.clip(grad)"))
        # try/finally restoring train mode, no clip call → False.
        self.assertFalse(catches_around_clip(
            "try:\n    run_validation()\nfinally:\n    model.train()"))
        # try/finally (NO handlers) that DOES contain a clip call → False:
        # a handler-less finally cannot swallow a signal, so this is the legal
        # form 40-05 requires (restore model.train() after the validation pass).
        self.assertFalse(catches_around_clip(
            "try:\n    outcome = clipper.clip(grad)\n    apply(outcome)\nfinally:\n    model.train()"))
        # Innocent code → False.
        self.assertFalse(catches_around_clip("x = clipper.norm(grad)"))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
