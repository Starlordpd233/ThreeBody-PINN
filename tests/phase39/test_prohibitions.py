"""Phase 39 mechanical boundary audit (Wave 0) — runs GREEN before production.

Two responsibilities:

1. **Real scans over the CURRENT tree.** The exact corpus-reader allowlist, the
   v1-ban, global-default, denominator-floor, footer/metrics-energy, s0-mutation
   and sole-classifier audits are evaluated over the discovered ``pinn/**/*.py``
   set today. They pass now because the only corpus reader is the retained
   Phase 38 probe ``pinn/verification/fixture_loader.py`` (GAP-39-02) and no
   ``pinn/data`` module exists yet. Discovery and the known-module superset
   become strict as each Wave-1+ file lands (39-01-PLAN task 39-01-02).

2. **Self-verification of every detector.** Because production code does not
   exist at Wave 0, each mechanical check is additionally proven against a
   SYNTHETIC violating source, so the gate is demonstrably able to FAIL on an
   injected corpus write, unauthorized reader, v1 import, global-default
   mutation, denominator floor, footer/metrics energy gate, s0 mutation, or a
   numeric stage classifier outside ``pinn/data/stages.py``.

Plus the ``TinyCorpus`` fixture contract (determinism, read-only containment,
the README 4->2 mapping, and the asymmetric pairing cases).

Grounding: ``39-PATTERNS.md`` (Mechanical prohibition audit), GAP-39-02 sole
reader, GAP-39-08 sole classifier, ``tests/phase38/test_prohibitions.py``.
"""

from __future__ import annotations

import ast
import importlib
import pathlib
import re
import unittest

from tests.phase39 import _SKIP_PHRASE
from tests.phase39 import _fixtures

ROOT = pathlib.Path(__file__).resolve().parents[2]

# GAP-39-02: the exact permitted corpus-reader set. ``adapter.py`` is the new
# production reader (may not exist yet); ``fixture_loader.py`` is the sole
# retained Phase 38 probe exception.
ALLOWED_CORPUS_READERS = {
    "pinn/data/adapter.py",
    "pinn/verification/fixture_loader.py",
}

# Every Wave-1+ production module the discovered set must eventually cover.
EXPECTED_DATA_MODULES = {
    "pinn/data/types.py",
    "pinn/data/preprocessing.py",
    "pinn/data/admission.py",
    "pinn/data/stages.py",
    "pinn/data/adapter.py",
    "pinn/data/splits.py",
    "pinn/data/batches.py",
    "pinn/data/stage_scan.py",
}

# The one module allowed to own numeric Stage-0/1 invariant predicates.
SOLE_CLASSIFIER = "pinn/data/stages.py"

_CORPUS_TOKENS = ("brutus_hierarchical", "brutus_standard", "ic_hierarchical", "ic_standard", ".txt")
_V1_TOKENS = ("data-handling", "data_handling", "data-processing-pipeline-full",
              "data_processing_pipeline_full", "basic_architecture")
_GLOBAL_DEFAULT_TOKENS = ("set_default_dtype", "is_available")


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
# Pure mechanical detectors (each is self-tested below).
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


def parses_corpus(exec_src):
    return any(tok in exec_src for tok in _CORPUS_TOKENS)


def has_v1_import(exec_src):
    return any(tok in exec_src for tok in _V1_TOKENS)


def has_global_default_mutation(exec_src):
    return any(tok in exec_src for tok in _GLOBAL_DEFAULT_TOKENS)


def has_denominator_floor(exec_src):
    """Detect a conservation denominator floor around ``H0`` (GAP-39-04 forbids
    additive epsilon / max / clamp / clip / fallback denominators)."""
    if any(tok in exec_src for tok in ("clamp", "clip", "maximum", "np.max(np.abs(H0")):
        return True
    # Adding anything to the H0 denominator, or a Python ``H0 or`` fallback.
    if re.search(r"H0\s*\+", exec_src) or re.search(r"\+\s*H0\b", exec_src):
        return True
    if re.search(r"H0\s+or\b", exec_src):
        return True
    return False


def has_footer_or_metrics_energy_gate(exec_src):
    """Detect gating on the Brutus footer ``dE/E`` or the metrics JSON energy
    (the gate must recompute eps_H from raw arrays — DATA-02 prohibitions)."""
    return ("dE/E" in exec_src or "sim_result_metric" in exec_src
            or "E_final" in exec_src or "E_initial" in exec_src)


def has_s0_mutation(exec_src):
    """Detect a code path that reassigns / ratifies the interim ``s0`` seam."""
    if "ratify" in exec_src or "ratified_s0" in exec_src:
        return True
    return bool(re.search(r"\b(interim_s0|s0)\s*=(?!=)", exec_src))


def owns_numeric_stage_classifier(exec_src):
    """Detect a numeric Stage-0/1 classifier (the ``s_min`` predicate producing
    a STAGE_0/STAGE_1 label) — permitted ONLY in ``pinn/data/stages.py``."""
    return "s_min" in exec_src and ("STAGE_0" in exec_src or "STAGE_1" in exec_src)


def target_under(root, target):
    """True iff ``target`` resolves beneath ``root`` (write-spy containment)."""
    try:
        pathlib.Path(target).resolve().relative_to(pathlib.Path(root).resolve())
    except (ValueError, OSError):
        return False
    return True


# ---------------------------------------------------------------------------
# Discovery.
# ---------------------------------------------------------------------------

_LEGACY = {
    "pinn/basic_architecture.py",
    "pinn/data-processing-pipeline-full.py",
    "pinn/runtime.py",
    "pinn/verification/componentwise_ad.py",
}


def discover_pinn_modules():
    out = []
    for path in sorted((ROOT / "pinn").rglob("*.py")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.endswith("__init__.py") or "data-handling" in rel.split("/") or rel in _LEGACY:
            continue
        out.append(path)
    return out


def discover_data_modules():
    return [p for p in discover_pinn_modules()
            if p.relative_to(ROOT).as_posix().startswith("pinn/data/")]


# ===========================================================================
# Real scans over the current tree.
# ===========================================================================

class SoleReaderAuditTests(unittest.TestCase):
    def test_only_allowed_modules_parse_the_corpus(self):
        offenders = []
        for path in discover_pinn_modules():
            rel = path.relative_to(ROOT).as_posix()
            if parses_corpus(executable_source(path)) and rel not in ALLOWED_CORPUS_READERS:
                offenders.append(rel)
        self.assertEqual(offenders, [], f"unauthorized corpus readers: {offenders}")

    def test_fixture_loader_is_recognized_as_the_probe_exception(self):
        rel = "pinn/verification/fixture_loader.py"
        self.assertTrue((ROOT / rel).is_file())
        self.assertTrue(parses_corpus(executable_source(ROOT / rel)))
        self.assertIn(rel, ALLOWED_CORPUS_READERS)


class ScopedDataModuleAuditTests(unittest.TestCase):
    """Scoped bans over ``pinn/data/**`` (vacuous now; strict as files land)."""

    def test_no_v1_import_in_data_modules(self):
        for path in discover_data_modules():
            self.assertFalse(has_v1_import(executable_source(path)),
                             f"{path} imports banned v1 data-handling/legacy pipeline")

    def test_no_global_default_mutation_in_data_modules(self):
        for path in discover_data_modules():
            self.assertFalse(has_global_default_mutation(executable_source(path)),
                             f"{path} mutates a global torch/device default")

    def test_no_denominator_floor_in_admission(self):
        adm = ROOT / "pinn/data/admission.py"
        if adm.is_file():
            self.assertFalse(has_denominator_floor(executable_source(adm)),
                             "admission.py introduces a conservation denominator floor")

    def test_no_footer_or_metrics_energy_gate_in_admission(self):
        adm = ROOT / "pinn/data/admission.py"
        if adm.is_file():
            self.assertFalse(has_footer_or_metrics_energy_gate(executable_source(adm)),
                             "admission.py gates on footer dE/E or metrics-JSON energy")

    def test_no_s0_mutation_in_data_modules(self):
        for path in discover_data_modules():
            self.assertFalse(has_s0_mutation(executable_source(path)),
                             f"{path} mutates/ratifies the interim s0 seam")

    def test_only_stages_owns_the_numeric_classifier(self):
        for path in discover_data_modules():
            rel = path.relative_to(ROOT).as_posix()
            if rel == SOLE_CLASSIFIER:
                continue
            self.assertFalse(owns_numeric_stage_classifier(executable_source(path)),
                             f"{rel} owns a numeric Stage-0/1 classifier (only "
                             f"{SOLE_CLASSIFIER} may)")

    def test_discovered_set_is_superset_of_present_expected_data_modules(self):
        discovered = {p.relative_to(ROOT).as_posix() for p in discover_pinn_modules()}
        present_expected = {m for m in EXPECTED_DATA_MODULES if (ROOT / m).is_file()}
        self.assertLessEqual(present_expected, discovered,
                             f"expected data modules missing from glob: "
                             f"{present_expected - discovered}")


# ===========================================================================
# Self-verification: every detector must FAIL on an injected violation.
# ===========================================================================

class DetectorSelfTests(unittest.TestCase):
    def test_executable_source_strips_docstrings_and_comments(self):
        src = executable_source_from_text(
            '"""set_default_dtype in a docstring is inert."""\n'
            "# is_available in a comment is inert\n"
            "x = 1\n")
        self.assertNotIn("set_default_dtype", src)
        self.assertNotIn("is_available", src)
        self.assertIn("x = 1", src)

    def test_unauthorized_reader_detected(self):
        self.assertTrue(parses_corpus('p = root / "brutus_hierarchical" / f.txt'))
        self.assertTrue(parses_corpus('re.compile(r"brutus_standard_(\\d{4})\\.txt")'))
        self.assertFalse(parses_corpus("x = tensor + 1"))

    def test_v1_import_detected(self):
        self.assertTrue(has_v1_import("from pinn.data_handling.core import parsing"))
        self.assertTrue(has_v1_import("import basic_architecture"))
        self.assertFalse(has_v1_import("from pinn.data.types import RecordKey"))

    def test_global_default_mutation_detected(self):
        self.assertTrue(has_global_default_mutation("torch.set_default_dtype(torch.float32)"))
        self.assertTrue(has_global_default_mutation("torch.backends.mps.is_available()"))
        self.assertFalse(has_global_default_mutation("tensor.to(dtype=dtype, device=device)"))

    def test_denominator_floor_detected(self):
        self.assertTrue(has_denominator_floor("eps_H = np.max(np.abs((H - H0) / (H0 + 1e-30)))"))
        self.assertTrue(has_denominator_floor("den = np.maximum(np.abs(H0), 1e-12)"))
        self.assertTrue(has_denominator_floor("den = H0 or 1e-12"))
        self.assertFalse(has_denominator_floor("eps_H = np.max(np.abs((H - H0) / H0))"))

    def test_footer_metrics_energy_gate_detected(self):
        self.assertTrue(has_footer_or_metrics_energy_gate("if footer['dE/E'] > 1e-5: reject()"))
        self.assertTrue(has_footer_or_metrics_energy_gate('json.load(open("sim_result_metric_0.json"))'))
        self.assertFalse(has_footer_or_metrics_energy_gate("eps_H = max_relative_drift(H)"))

    def test_s0_mutation_detected(self):
        self.assertTrue(has_s0_mutation("interim_s0 = 0.02"))
        self.assertTrue(has_s0_mutation("ratify(s0)"))
        self.assertFalse(has_s0_mutation("def classify(record, s0): return record.s_min > s0"))

    def test_numeric_classifier_detected(self):
        self.assertTrue(owns_numeric_stage_classifier(
            "if record.s_min > s0 and cond: return StageLabel.STAGE_0"))
        self.assertFalse(owns_numeric_stage_classifier("return persisted.stage_label"))

    def test_write_spy_containment_detects_escape(self):
        forbidden = _fixtures.simulation_data_root(ROOT)
        self.assertTrue(target_under(forbidden, forbidden / "Data" / "brutus_output" / "x.txt"))
        self.assertFalse(target_under(forbidden, ROOT / "tests" / "phase39" / "x.txt"))


# ===========================================================================
# TinyCorpus fixture contract (Task 39-01-02 acceptance criteria 1-3).
# ===========================================================================

class TinyCorpusContractTests(unittest.TestCase):
    def test_deterministic_relative_bytes_across_two_builds(self):
        with _fixtures.TinyCorpus() as a, _fixtures.TinyCorpus() as b:
            self.assertEqual(a.relative_manifest(), b.relative_manifest())
            # Sparse IDs and base/gold siblings are present.
            self.assertTrue(any("brutus_hierarchical_0042" in k for k in a.relative_manifest()))
            self.assertTrue(any("gold_standard/brutus_hierarchical_0000" in k
                                for k in a.relative_manifest()))

    def test_every_created_path_is_outside_simulation_data(self):
        forbidden = _fixtures.simulation_data_root(ROOT)
        with _fixtures.TinyCorpus() as corpus:
            self.assertTrue(corpus.created_paths)
            for path in corpus.created_paths:
                self.assertTrue(_fixtures.path_is_outside(path, forbidden),
                                f"fixture wrote beneath simulation_data/: {path}")

    def test_models_four_to_two_brutus_to_ic_mapping(self):
        with _fixtures.TinyCorpus() as corpus:
            ic_root = corpus.data_root / _fixtures.IC_SUBDIR
            brutus_root = corpus.data_root / _fixtures.BRUTUS_SUBDIR
            ic_folders = sorted(p.name for p in ic_root.iterdir() if p.is_dir())
            brutus_folders = sorted(p.name for p in brutus_root.iterdir() if p.is_dir())
            self.assertEqual(ic_folders, sorted(_fixtures.IC_FOLDERS))
            self.assertEqual(brutus_folders, sorted(_fixtures.BRUTUS_FOLDERS))
            # No ``_for_gold_standard`` IC folder exists.
            self.assertFalse(any("for_gold_standard" in name for name in ic_folders))

    def test_gold_brutus_pairs_to_a_base_ic_record(self):
        """HIGH-3: a 1:1-folder-pairing assumption would mass-quarantine this."""
        with _fixtures.TinyCorpus() as corpus:
            variant, id_ = corpus.gold_with_base_ic
            gold = corpus._brutus_path("brutus_hierarchical_gold_standard", variant, id_)
            base_ic = corpus._ic_path(variant, id_)
            self.assertTrue(gold.is_file())
            self.assertTrue(base_ic.is_file(),
                            "gold Brutus id has no BASE IC — HIGH-3 fixture broken")

    def test_asymmetric_pairing_cases_present(self):
        with _fixtures.TinyCorpus() as corpus:
            # Brutus present with no matching IC.
            bv, bid = corpus.brutus_without_ic
            self.assertTrue(corpus._brutus_path("brutus_hierarchical", bv, bid).is_file())
            self.assertFalse(corpus._ic_path(bv, bid).is_file())
            # IC present with no matching Brutus (base or gold).
            iv, iid = corpus.ic_without_brutus
            self.assertTrue(corpus._ic_path(iv, iid).is_file())
            self.assertFalse(corpus._brutus_path("brutus_hierarchical", iv, iid).is_file())
            self.assertFalse(
                corpus._brutus_path("brutus_hierarchical_gold_standard", iv, iid).is_file())

    def test_valid_and_invalid_blacklist_and_version_metadata_exist(self):
        with _fixtures.TinyCorpus() as corpus:
            self.assertTrue(corpus.blacklist_path.is_file())
            self.assertTrue(corpus.invalid_blacklist_path.is_file())
            self.assertTrue(corpus.version_metadata_path.is_file())
            self.assertFalse(corpus.absent_version_metadata_path.exists())


# ===========================================================================
# Task 39-03-03 — integration containment gate (adapter/preprocessing/stages/
# admission now all exist).
# ===========================================================================

class IntegrationContainmentTests(unittest.TestCase):
    """With the Wave-1..3 production modules landed, tighten the sole-reader /
    sole-classifier / single-glob audits into strict positive assertions."""

    def test_adapter_is_the_only_data_module_that_parses_or_globs_the_corpus(self):
        offenders = []
        for path in discover_data_modules():
            rel = path.relative_to(ROOT).as_posix()
            if rel == "pinn/data/adapter.py":
                continue
            src = executable_source(path)
            if parses_corpus(src) or "glob(" in src or "rglob(" in src:
                offenders.append(rel)
        self.assertEqual(offenders, [], f"non-adapter data modules read/glob the corpus: {offenders}")

    def test_adapter_module_actually_scans_the_corpus(self):
        # Positive assertion: the sole reader really does own the glob/parse path.
        adapter_src = executable_source(ROOT / "pinn/data/adapter.py")
        self.assertTrue(parses_corpus(adapter_src))
        self.assertIn("glob(", adapter_src)

    def test_adapter_does_not_own_the_numeric_stage_classifier(self):
        # The adapter reads ``.s_min`` off its interim classify record but must
        # NOT own the STAGE_0/STAGE_1 predicate — that lives only in stages.py.
        adapter_src = executable_source(ROOT / "pinn/data/adapter.py")
        self.assertFalse(owns_numeric_stage_classifier(adapter_src))

    def test_stages_remains_the_sole_numeric_classifier_among_present_modules(self):
        owners = [p.relative_to(ROOT).as_posix() for p in discover_data_modules()
                  if owns_numeric_stage_classifier(executable_source(p))]
        self.assertEqual(owners, [SOLE_CLASSIFIER])

    def test_all_present_expected_data_modules_are_covered_by_discovery(self):
        discovered = {p.relative_to(ROOT).as_posix() for p in discover_pinn_modules()}
        present_expected = {m for m in EXPECTED_DATA_MODULES if (ROOT / m).is_file()}
        # Wave-1..3 modules exist; Wave-4..6 (splits/batches/stage_scan) do not yet.
        self.assertIn("pinn/data/adapter.py", present_expected)
        self.assertIn("pinn/data/stages.py", present_expected)
        self.assertLessEqual(present_expected, discovered)


# ===========================================================================
# Deferred adapter-level write/containment audits (skip until adapter lands).
# ===========================================================================

class DeferredAdapterReadOnlyTests(unittest.TestCase):
    def test_adapter_never_writes_under_the_corpus_or_simulation_data(self):
        AdmittedSetAdapter = _require("AdmittedSetAdapter", "pinn.data.adapter")
        import builtins
        import os

        forbidden_roots = [_fixtures.simulation_data_root(ROOT)]
        write_hits: list[str] = []
        real_open, real_mkdir, real_makedirs = builtins.open, os.mkdir, os.makedirs

        def _flag(target):
            for froot in forbidden_roots:
                if target_under(froot, target):
                    write_hits.append(str(target))

        def spy_open(file, mode="r", *a, **k):
            if any(f in str(mode) for f in ("w", "a", "x", "+")):
                _flag(file)
            return real_open(file, mode, *a, **k)

        with _fixtures.TinyCorpus() as corpus:
            forbidden_roots.append(corpus.data_root.resolve())
            builtins.open = spy_open
            os.mkdir = lambda p, *a, **k: (_flag(p), real_mkdir(p, *a, **k))[1]
            os.makedirs = lambda p, *a, **k: (_flag(p), real_makedirs(p, *a, **k))[1]
            try:
                AdmittedSetAdapter(root=corpus.data_root, blacklist_path=corpus.blacklist_path,
                                   precision="float32", device="cpu", run_dir=corpus.run_dir)
            finally:
                builtins.open, os.mkdir, os.makedirs = real_open, real_mkdir, real_makedirs
        self.assertEqual(write_hits, [], f"adapter wrote to a read-only root: {write_hits}")

    def test_adapter_rejects_a_root_containment_escape(self):
        AdmittedSetAdapter = _require("AdmittedSetAdapter", "pinn.data.adapter")
        with _fixtures.TinyCorpus() as corpus:
            with self.assertRaises((ValueError, OSError)):
                AdmittedSetAdapter(root=corpus.data_root / ".." / "escape",
                                   blacklist_path=corpus.blacklist_path,
                                   precision="float32", device="cpu", run_dir=corpus.run_dir)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
