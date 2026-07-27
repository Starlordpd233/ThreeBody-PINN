"""Dataset-free INST-01 isolation / restoration / non-interference suite (plan 46-05, Task 1).

Proves — rather than asserts — the D-12/D-15/D-16/D-23 safety properties of
``pinn/training/validation_gate.py``:

- **Held-out isolation (D-16)** is enforced twice, so neither a lazy import nor
  a transitive import escapes detection (T-46-05-01): an AST scan of the raw
  module source finds no import resolving to the held-out evaluator module, AND
  a fresh-subprocess import of the gate leaves the evaluator's dotted module
  name absent from ``sys.modules``.
- **Prior-mode restoration (D-12)** is proven from BOTH prior states and under
  an injected mid-population failure, and the mode bracket is AST-pinned as a
  handler-less ``try/finally`` (a bare ``try/finally`` cannot swallow a signal;
  only an ``except`` handler can — the phase40 detector convention).
- **Non-interference (D-15)** is proven bitwise (parameters identical, no
  populated gradient, around a real tiny-network gate pass), structurally (the
  call signature admits no optimizer/scheduler/stage-machine/replay/checkpoint
  object), and behaviorally (two consecutive passes are identical).

Dataset-free (D-24): no real corpus and no production run directory is read;
every population is the 46-01 disjoint stub pair.

Frame input rule: every ``compute_validation_gate`` call here takes an explicit
coherent ``FrameConvention`` constructed INLINE in this module — the properties
are frame-independent (D-07). The wave-5 production ratified-frame constant
does not exist while this wave executes and is never referenced: reaching for
it through ``_require`` would convert every test in this suite into a vacuous
skip that still exits green (T-46-05-04).

The production module is present (46-03 landed in wave 2), so every test RUNS
— none skip. The ``_require`` helper exists so a wave-misordered checkout
degrades to a localized skip (never an import ERROR), per the tests/phase46
convention.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import pathlib
import re
import subprocess
import sys
import unittest

import torch

from tests.phase40._fixtures import make_stub_model
from tests.phase46 import _SKIP_PHRASE
from tests.phase46._fixtures import StubModel, make_stub_split_sources

ROOT = pathlib.Path(__file__).resolve().parents[2]

_VG_MODULE = "pinn.training.validation_gate"
_VG_PATH = ROOT / "pinn" / "training" / "validation_gate.py"
_EVALUATOR_MODULE = "pinn.evaluate"


def _require(symbol, module):
    """Per-symbol deferred import — SkipTest (never ERROR) until it lands."""
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)


FrameConvention = _require("FrameConvention", _VG_MODULE)
compute_validation_gate = _require("compute_validation_gate", _VG_MODULE)
POSITION_FRAME_SCALED = _require("POSITION_FRAME_SCALED", _VG_MODULE)
TIME_COORD_NORMALIZED = _require("TIME_COORD_NORMALIZED", _VG_MODULE)
MASS_CONVENTION_ORDERED_RAW = _require("MASS_CONVENTION_ORDERED_RAW", _VG_MODULE)

# The inline coherent frame (D-07 frame-independence): built from the module's
# own constants HERE, never from the wave-5 production constant.
SCALED_FRAME = FrameConvention(
    POSITION_FRAME_SCALED,
    TIME_COORD_NORMALIZED,
    MASS_CONVENTION_ORDERED_RAW,
    conf01_evidence_ref="phase46-05-isolation-fixture",
)


# ---------------------------------------------------------------------------
# Source helpers (AST-over-raw-source, mirroring the phase40 detector style)
# ---------------------------------------------------------------------------


def _module_source_text():
    """Raw ``validation_gate`` source text; SkipTest (never ERROR) while absent."""
    if not _VG_PATH.is_file():
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {_VG_MODULE} (source file)")
    return _VG_PATH.read_text(encoding="utf-8")


def _absolute_importfrom_module(node):
    """Resolve an ``ImportFrom`` node's module to its absolute dotted name.

    ``node.level == 0`` is already absolute. Relative levels resolve against the
    package containing ``validation_gate`` (``pinn.training``): level 1 is the
    package itself, level 2 its parent — so ``from .. import evaluate`` inside
    the module resolves to ``pinn`` + ``evaluate`` and is caught below.
    """
    if node.level == 0:
        return node.module or ""
    parts = _VG_MODULE.split(".")[:-1]
    if node.level - 1 > len(parts):
        return node.module or ""
    base = parts[: len(parts) - (node.level - 1)]
    if node.module:
        base = base + node.module.split(".")
    return ".".join(base)


def _import_nodes_targeting_evaluator(tree):
    """Return Import/ImportFrom nodes that resolve to the evaluator module.

    Every spelling is covered: ``import pinn.evaluate[.x]``,
    ``from pinn.evaluate[.x] import ...``, ``from pinn import evaluate``, and
    the relative forms (``from .. import evaluate`` resolves to ``pinn`` and is
    caught by the package-plus-name check).
    """
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == _EVALUATOR_MODULE or alias.name.startswith(
                    _EVALUATOR_MODULE + "."
                ):
                    hits.append(node)
                    break
        elif isinstance(node, ast.ImportFrom):
            module = _absolute_importfrom_module(node)
            if module == _EVALUATOR_MODULE or module.startswith(_EVALUATOR_MODULE + "."):
                hits.append(node)
            elif module == "pinn" and any(
                alias.name == "evaluate" for alias in node.names
            ):
                hits.append(node)
    return hits


def _calls_bare_model(node):
    """True if ``node``'s subtree contains a bare ``model(...)`` call.

    Attribute calls (``model.train()`` / ``model.eval()``) do NOT match: their
    func is an ``Attribute``, so a restoration statement in a ``finally`` body
    is never mistaken for the forward pass.
    """
    return any(
        isinstance(child, ast.Call)
        and isinstance(child.func, ast.Name)
        and child.func.id == "model"
        for child in ast.walk(node)
    )


def _mode_bracket_try(tree):
    """The ``Try`` node in ``compute_validation_gate`` whose BODY reaches the model call."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name != "compute_validation_gate":
                continue
            for child in ast.walk(node):
                if isinstance(child, ast.Try) and any(
                    _calls_bare_model(stmt) for stmt in child.body
                ):
                    return child
    return None


def _mid_pass_failure(*, fail_on_call=2):
    """A StubModel fail_hook that lets one record through, then raises mid-pool."""
    state = {"calls": 0}

    def hook(_model):
        state["calls"] += 1
        if state["calls"] >= fail_on_call:
            raise RuntimeError("injected mid-pass failure")

    return hook


# ---------------------------------------------------------------------------
# D-16 — held-out isolation, enforced statically AND transitively
# ---------------------------------------------------------------------------


class EvaluatorImportIsolationTests(unittest.TestCase):
    """D-16: the gate never imports the held-out evaluator — proven twice."""

    def test_ast_scan_finds_no_evaluator_import(self):
        tree = ast.parse(_module_source_text(), filename=str(_VG_PATH))
        hits = _import_nodes_targeting_evaluator(tree)
        self.assertEqual(
            hits,
            [],
            f"{_VG_MODULE} imports the held-out evaluator "
            f"{_EVALUATOR_MODULE!r} at line(s) "
            f"{[getattr(node, 'lineno', '?') for node in hits]} (D-16)",
        )

    def test_fresh_subprocess_import_leaves_evaluator_absent(self):
        # The TRANSITIVE import graph stays clean, not just the direct source:
        # a fresh interpreter imports the gate and reports whether any
        # evaluator module (exact or submodule) landed in sys.modules.
        code = (
            "import sys\n"
            "sys.path.insert(0, '.')\n"
            "import pinn.training.validation_gate\n"
            "bad = [m for m in sys.modules\n"
            "       if m == 'pinn.evaluate' or m.startswith('pinn.evaluate.')]\n"
            "print('present' if bad else 'absent')\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            timeout=180,
        )
        self.assertEqual(
            result.returncode, 0, msg=f"isolation subprocess failed:\n{result.stderr}"
        )
        self.assertEqual(
            result.stdout.strip(),
            "absent",
            f"importing {_VG_MODULE} pulled the held-out evaluator into "
            f"sys.modules (D-16); stderr:\n{result.stderr}",
        )


# ---------------------------------------------------------------------------
# D-12 / D-23 — prior-mode restoration, healthy and under failure
# ---------------------------------------------------------------------------


class ModeRestorationTests(unittest.TestCase):
    """D-12/D-23: the PRIOR mode is restored — strictly stronger than an
    unconditional ``train()`` restore, and proven from both prior states."""

    @classmethod
    def setUpClass(cls):
        # Three validation records: the fail hook fires on call 2 of 3, so the
        # failure is genuinely MID-population, never at the boundary.
        cls.validation_source = make_stub_split_sources(
            n_train=2, n_validation=3, n_snapshots=8
        )[1]

    def test_prior_train_mode_restored_after_healthy_pass(self):
        model = StubModel()
        model.train()
        compute_validation_gate(
            model, self.validation_source, stage=0, global_step=0, frame=SCALED_FRAME
        )
        self.assertTrue(model.training)

    def test_prior_eval_mode_restored_after_healthy_pass(self):
        model = StubModel()
        model.eval()
        compute_validation_gate(
            model, self.validation_source, stage=0, global_step=0, frame=SCALED_FRAME
        )
        self.assertFalse(model.training)

    def test_prior_train_mode_restored_under_injected_failure(self):
        model = StubModel(fail_hook=_mid_pass_failure())
        model.train()
        with self.assertRaises(RuntimeError):
            compute_validation_gate(
                model, self.validation_source, stage=0, global_step=0, frame=SCALED_FRAME
            )
        self.assertEqual(len(model.calls), 2, "failure must land mid-population")
        self.assertTrue(model.training)

    def test_prior_eval_mode_restored_under_injected_failure(self):
        model = StubModel(fail_hook=_mid_pass_failure())
        model.eval()
        with self.assertRaises(RuntimeError):
            compute_validation_gate(
                model, self.validation_source, stage=0, global_step=0, frame=SCALED_FRAME
            )
        self.assertEqual(len(model.calls), 2, "failure must land mid-population")
        self.assertFalse(model.training)

    def test_mode_bracket_is_handler_less_try_finally(self):
        # Mirrors the phase40 detector's scoping rule: a handler-less
        # try/finally cannot swallow a signal — only an except handler can.
        tree = ast.parse(_module_source_text(), filename=str(_VG_PATH))
        bracket = _mode_bracket_try(tree)
        self.assertIsNotNone(
            bracket, "compute_validation_gate has no try whose body reaches the model call"
        )
        self.assertEqual(
            bracket.handlers,
            [],
            "the mode bracket must be handler-less: an except clause could "
            "swallow the mid-pass signal this suite proves propagates",
        )
        self.assertTrue(
            bracket.finalbody,
            "the mode bracket must restore the prior mode in a finally body",
        )


# ---------------------------------------------------------------------------
# D-15 / D-23 — observation-only non-interference
# ---------------------------------------------------------------------------


class NonInterferenceTests(unittest.TestCase):
    """D-15/D-23: the pass touches no training state — bitwise, structural,
    and behavioral proof."""

    @classmethod
    def setUpClass(cls):
        cls.validation_source = make_stub_split_sources(
            n_train=2, n_validation=3, n_snapshots=8
        )[1]

    def test_parameters_bitwise_identical_and_grad_free_after_pass(self):
        model = make_stub_model()  # tiny real network, CPU/float64
        before = [p.detach().clone() for p in model.parameters()]
        compute_validation_gate(
            model, self.validation_source, stage=0, global_step=0, frame=SCALED_FRAME
        )
        params = list(model.parameters())
        self.assertEqual(len(before), len(params))
        for index, (old, new) in enumerate(zip(before, params)):
            self.assertTrue(
                torch.equal(old, new),
                f"parameter {index} was mutated by the gate pass (D-15)",
            )
        for index, p in enumerate(params):
            self.assertIsNone(
                p.grad, f"parameter {index} holds a populated gradient (D-15)"
            )

    def test_signature_admits_no_interference_channel(self):
        # Pin the exact parameter list: an interference-capable argument
        # (optimizer, scheduler, stage machine, replay, checkpoint, early-stop)
        # cannot be added silently.
        signature = inspect.signature(compute_validation_gate)
        params = list(signature.parameters.values())
        self.assertEqual(
            [p.name for p in params],
            ["model", "validation_source", "stage", "global_step", "frame", "dtype", "device"],
        )
        for p in params[:2]:
            self.assertEqual(p.kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        for p in params[2:]:
            self.assertEqual(
                p.kind,
                inspect.Parameter.KEYWORD_ONLY,
                f"{p.name} must stay keyword-only",
            )
        banned = (
            "optimizer", "scheduler", "replay", "checkpoint", "early_stop",
            "stage_machine", "stage_exit", "curriculum", "controller",
            "loss", "grad", "hook", "callback", "writer",
        )
        for name in (p.name for p in params):
            for token in banned:
                self.assertNotIn(
                    token,
                    name.lower(),
                    f"parameter {name!r} names an interference channel (D-15)",
                )

    def test_consecutive_passes_are_deterministic(self):
        # The pass is deterministic and stateless over a fixed source/model:
        # two consecutive passes over the tiny real network agree exactly.
        model = make_stub_model()
        first = compute_validation_gate(
            model, self.validation_source, stage=0, global_step=0, frame=SCALED_FRAME
        )
        second = compute_validation_gate(
            model, self.validation_source, stage=0, global_step=0, frame=SCALED_FRAME
        )
        self.assertEqual(first.n_trajectories, second.n_trajectories)
        self.assertEqual(
            [row.record_key for row in first.rows],
            [row.record_key for row in second.rows],
        )
        for a, b in zip(first.rows, second.rows):
            self.assertEqual(a.eps_h, b.eps_h)
            self.assertEqual(a.scs, b.scs)
        self.assertEqual(first.aggregate_eps_h, second.aggregate_eps_h)
        self.assertEqual(first.aggregate_scs, second.aggregate_scs)
        self.assertEqual(first.verdict, second.verdict)


# ---------------------------------------------------------------------------
# D-16 / D-23 — validation-source-only driving + fixture-surface regression pin
# ---------------------------------------------------------------------------


class ValidationOnlySourceTests(unittest.TestCase):
    """D-16/D-23: the gate is driven ONLY by the validation member of the
    disjoint stub pair, and the fixture surface still offers no withheld-split
    constructor."""

    def test_gate_rows_come_only_from_validation_source(self):
        train_source, validation_source = make_stub_split_sources(
            n_train=3, n_validation=4, n_snapshots=8
        )
        train_keys = set(train_source.record_keys())
        validation_keys = set(validation_source.record_keys())
        self.assertTrue(
            train_keys,
            "train stub must be non-empty — two empty sets are trivially disjoint",
        )
        self.assertTrue(validation_keys)
        self.assertTrue(train_keys.isdisjoint(validation_keys))

        model = StubModel()
        observation = compute_validation_gate(
            model, validation_source, stage=0, global_step=0, frame=SCALED_FRAME
        )
        row_keys = [row.record_key for row in observation.rows]
        # Full-pool: every validation key appears, in sorted order (the stub's
        # descending insertion order makes this genuinely non-vacuous).
        self.assertEqual(len(row_keys), len(validation_keys))
        self.assertEqual(row_keys, sorted(validation_keys))
        for key in row_keys:
            self.assertIn(key, validation_keys)
            self.assertNotIn(key, train_keys)
        self.assertEqual(observation.split, "validation")

    def test_fixture_surface_has_no_withheld_split_constructor(self):
        # Regression-pin 46-01 acceptance criterion 3: the banned identifier
        # set still has zero matches in the fixture module — the absence is
        # re-asserted on source text, never by building the forbidden object
        # (D-16).
        fixtures_path = ROOT / "tests" / "phase46" / "_fixtures.py"
        self.assertTrue(fixtures_path.is_file())
        text = fixtures_path.read_text(encoding="utf-8")
        banned = re.compile(r"test_source|make_test|test_index|held.?out", re.IGNORECASE)
        matches = banned.findall(text)
        self.assertEqual(
            matches,
            [],
            f"withheld-split identifier(s) appeared in the fixture surface: {matches}",
        )


if __name__ == "__main__":
    unittest.main()
