"""Contract tests for the Phase 55 architecture characterization probe."""

from __future__ import annotations

import ast
import copy
import hashlib
import importlib
import json
import math
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import pytest
import torch

from pinn.loss_catalog import resolve_causal_clip_facts


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = "pinn.verification.architecture_characterization_probe"
FIXTURE_PATH = pathlib.Path(__file__).resolve().parent / "fixtures" / "six_case_baseline.json"


def _load_probe():
    """Defer production import so the RED suite skips before the module exists."""
    try:
        return importlib.import_module(MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{MODULE} has not landed yet: {exc}") from exc


def _tracer_case(probe):
    return probe.SweepCase(
        label="41",
        seed=41,
        masses=(1.0, 1.0, 1.0),
        ic13_mode="zero",
    )


def test_tracer_single_case_reports_all_seven_quantities():
    probe = _load_probe()
    result = probe.measure_case(_tracer_case(probe))

    assert isinstance(result, probe.ArchitectureCharacterizationResult)
    assert math.isfinite(result.r_norm_median)
    assert math.isfinite(result.v_norm_median)
    assert math.isfinite(result.a_norm_median)
    assert math.isfinite(result.f_grav_norm_median)
    assert math.isfinite(result.min_pairwise_separation_median)
    assert math.isfinite(result.rbar_median)
    assert isinstance(result.front_idx, int)
    assert result.front_idx == 0
    assert 1e9 < result.rbar_median < 1e11
    assert len(result.causal_weights) == result.n_col
    assert result.causal_weights[0] == 1.0
    times = result.collocation_times
    assert len(times) == result.n_col
    assert times == tuple(sorted(times))
    assert all(times[index] < times[index + 1] for index in range(len(times) - 1))


def test_tracer_case_is_deterministic_across_two_calls():
    probe = _load_probe()
    case = _tracer_case(probe)
    first = probe.measure_case(case)
    second = probe.measure_case(case)
    assert first == second


def test_sweep_case_rejects_malformed_fields():
    probe = _load_probe()
    SweepCase = probe.SweepCase
    valid = dict(label="41", seed=41, masses=(1.0, 1.0, 1.0), ic13_mode="zero")

    with pytest.raises(ValueError, match="label"):
        SweepCase(**{**valid, "label": ""})
    with pytest.raises(ValueError, match="label"):
        SweepCase(**{**valid, "label": 41})
    with pytest.raises(ValueError, match="seed"):
        SweepCase(**{**valid, "seed": -1})
    with pytest.raises(ValueError, match="seed"):
        SweepCase(**{**valid, "seed": True})
    with pytest.raises(ValueError, match="masses"):
        SweepCase(**{**valid, "masses": (1.0, 1.0)})
    with pytest.raises(ValueError, match="masses"):
        SweepCase(**{**valid, "masses": (1.0, 1.0, float("nan"))})
    with pytest.raises(ValueError, match="masses"):
        SweepCase(**{**valid, "masses": (1.0, 1.0, 0.0)})
    with pytest.raises(ValueError, match="ic13_mode"):
        SweepCase(**{**valid, "ic13_mode": "bogus"})


_AUDITED_ROWS = (
    ("41", 41, (1.0, 1.0, 1.0), "zero"),
    ("42", 42, (1.0, 1.0, 1.0), "zero"),
    ("43", 43, (1.0, 1.0, 1.0), "zero"),
    ("0", 0, (1.0, 1.0, 1.0), "zero"),
    ("7", 7, (1.0, 1.0, 1.0), "zero"),
    ("41-variable-mass", 41, (1.0, 0.8, 0.6), "random_tanh"),
)
_AUDITED_LABELS = tuple(row[0] for row in _AUDITED_ROWS)


@pytest.fixture(scope="module")
def default_sweep():
    probe = _load_probe()
    return probe, probe.run_sweep()


def test_default_cases_are_the_six_audited_rows(default_sweep):
    probe, results = default_sweep
    assert len(probe.DEFAULT_CASES) == 6
    assert len(results) == 6
    for case, result, expected in zip(probe.DEFAULT_CASES, results, _AUDITED_ROWS):
        label, seed, masses, ic13_mode = expected
        assert case.label == label
        assert case.seed == seed
        assert case.masses == masses
        assert case.ic13_mode == ic13_mode
        assert result.label == label
        assert result.seed == seed
        assert result.masses == masses
        assert result.ic13_mode == ic13_mode


@pytest.mark.parametrize("label", _AUDITED_LABELS)
def test_invariant_bounds_six_cases(default_sweep, label):
    _probe, results = default_sweep
    result = next(item for item in results if item.label == label)
    assert result.front_idx == 0
    assert 1e9 < result.rbar_median < 1e11
    assert 0.1 < result.f_grav_norm_median < 100
    assert result.min_pairwise_separation_median > 1e-2
    assert len(result.causal_weights) == 16


@pytest.mark.parametrize("label", _AUDITED_LABELS)
def test_causal_weights_pinned_at_dtype_clamp_floor(default_sweep, label):
    _probe, results = default_sweep
    floor = resolve_causal_clip_facts(
        torch.float64, torch.device("cpu")
    )["causal_clip_min_weight"]
    result = next(item for item in results if item.label == label)
    assert result.causal_weights[0] == 1.0
    assert all(weight == floor for weight in result.causal_weights[1:])
    assert result.causal_clip_min_weight == floor


@pytest.mark.parametrize("label", _AUDITED_LABELS)
def test_norm_convention_matches_audit_rbar_identity(default_sweep, label):
    _probe, results = default_sweep
    result = next(item for item in results if item.label == label)
    predicted = result.a_norm_median ** 2 / 3.0
    relative = abs(result.rbar_median - predicted) / result.rbar_median
    assert relative < 0.10


def test_front_idx_threshold_is_strictly_above_half():
    probe = _load_probe()
    above = float(np.nextafter(0.5, 1.0))
    # 0.5 sits at a higher index than 0.5+ulp; a >= predicate would return 2.
    assert probe._front_idx([above, 0.5, 0.5]) == 0


def test_front_idx_sentinel_when_no_weight_exceeds_half():
    probe = _load_probe()
    assert probe._front_idx([0.5, 0.4, 0.0, 0.5]) == -1


def test_median_convention_averages_two_central_values(default_sweep):
    probe, results = default_sweep
    values = (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 10.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0)
    assert probe._median(values) == 15.0
    assert "numpy.median" in probe.MEDIAN_CONVENTION
    assert "torch.median" in probe.MEDIAN_CONVENTION
    assert "arithmetic mean of the two central order statistics" in probe.MEDIAN_CONVENTION
    for result in results:
        assert result.median_convention == probe.MEDIAN_CONVENTION


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


def test_derives_from_trainer_implementation():
    probe = _load_probe()
    case = _tracer_case(probe)
    baseline = probe.measure_case(case)
    scale = 2.0

    original_causal = probe.causal_physics_loss

    def mutated_causal(*args, **kwargs):
        loss, details = original_causal(*args, **kwargs)
        details = dict(details)
        details["w_n"] = details["w_n"] * scale
        return loss, details

    with mock.patch.object(probe, "causal_physics_loss", side_effect=mutated_causal):
        mutated = probe.measure_case(case)
    for base_weight, mutated_weight in zip(baseline.causal_weights, mutated.causal_weights):
        assert mutated_weight / base_weight == pytest.approx(scale)

    original_force = probe.softened_acceleration

    def mutated_force(*args, **kwargs):
        return original_force(*args, **kwargs) * scale

    with mock.patch.object(probe, "softened_acceleration", side_effect=mutated_force):
        mutated = probe.measure_case(case)
    assert mutated.f_grav_norm_median / baseline.f_grav_norm_median == pytest.approx(scale)

    original_du = probe.componentwise_du

    def mutated_du(*args, **kwargs):
        first, second = original_du(*args, **kwargs)
        return first * scale, second * scale

    with mock.patch.object(probe, "componentwise_du", side_effect=mutated_du):
        mutated = probe.measure_case(case)
    assert mutated.v_norm_median / baseline.v_norm_median == pytest.approx(scale)
    assert mutated.a_norm_median / baseline.a_norm_median == pytest.approx(scale)


def test_module_has_no_global_default_mutation_or_device_probe():
    # Re-homed from tests/phase38/test_prohibitions.py
    # (test_no_precision_default_in_discovered_modules's set_default_dtype /
    # is_available checks). Plan 55-02 will exclude this module from that glob;
    # these two guarantees are preserved here rather than duplicated as a glob
    # scan. The argparse-precision-default check is surrendered deliberately
    # because CONTEXT.md D-02 requires a defaulted --precision flag.
    probe = _load_probe()
    executable = _executable_source(pathlib.Path(probe.__file__).resolve())
    assert "set_default_dtype" not in executable
    assert "is_available" not in executable


def test_module_has_no_v1_3_era_imports():
    # Re-homed from tests/phase38/test_prohibitions.py
    # (test_no_v1_3_era_imports_in_discovered_modules). Same exclusion note as
    # test_module_has_no_global_default_mutation_or_device_probe: these tokens
    # are preserved locally rather than remaining on the Phase-38 glob.
    probe = _load_probe()
    executable = _executable_source(pathlib.Path(probe.__file__).resolve())
    banned_tokens = (
        "basic_architecture",
        "data-processing-pipeline-full",
        "data_processing_pipeline_full",
        "data-handling",
        "data_handling",
    )
    for token in banned_tokens:
        assert token not in executable


_MALFORMED_CASES_CONFIG = (
    ({"label": "x", "seed": -1, "masses": [1.0, 1.0, 1.0], "ic13_mode": "zero"}, "seed"),
    ({"label": "x", "seed": True, "masses": [1.0, 1.0, 1.0], "ic13_mode": "zero"}, "seed"),
    ({"label": "x", "seed": 1, "masses": [1.0, 1.0], "ic13_mode": "zero"}, "masses"),
    ({"label": "x", "seed": 1, "masses": [1.0, 1.0, 0.0], "ic13_mode": "zero"}, "masses"),
    ({"label": "x", "seed": 1, "masses": [1.0, 1.0, 1.0], "ic13_mode": "bogus"}, "ic13_mode"),
)


@pytest.mark.parametrize("payload,field", _MALFORMED_CASES_CONFIG)
def test_malformed_cases_config_raises_value_error(payload, field, tmp_path):
    probe = _load_probe()
    config_path = tmp_path / "cases.json"
    config_path.write_text(json.dumps([payload]), encoding="utf-8")
    evidence_root = tmp_path / "evidence"
    evidence_root.mkdir()
    with pytest.raises(ValueError, match=field):
        probe.load_cases_config(config_path)
    assert list(evidence_root.iterdir()) == []


class ArchitectureCharacterizationCLITests(unittest.TestCase):
    """CLI-subprocess contract: module entry point, evidence, non-verdict exit."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="phase55-probe-")
        self.addCleanup(self._tmp.cleanup)
        self.tmp = pathlib.Path(self._tmp.name)

    def _evidence_root(self, name: str) -> pathlib.Path:
        return self.tmp / "evidence" / name

    def _run_cli(self, evidence_root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", MODULE, *args, "--evidence-root", str(evidence_root)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    @staticmethod
    def _only_raw(evidence_root: pathlib.Path) -> dict:
        raw_paths = sorted(evidence_root.glob("*/raw.json"))
        if len(raw_paths) != 1:
            raise AssertionError(
                f"expected one evidence run under {evidence_root}, found {raw_paths}"
            )
        return json.loads(raw_paths[0].read_text(encoding="utf-8"))

    def test_zero_argument_cli_reproduces_six_rows(self):
        probe = _load_probe()
        root = self._evidence_root("zero-arg")
        completed = self._run_cli(root)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        raw = self._only_raw(root)
        self.assertEqual(
            [case["label"] for case in raw["cases"]],
            [case.label for case in probe.DEFAULT_CASES],
        )
        self.assertTrue((next(root.glob("*/raw.json")).parent / "summary.md").is_file())

    def test_cases_config_drives_arbitrary_case_list(self):
        _load_probe()
        root = self._evidence_root("two-cases")
        config_path = self.tmp / "two.json"
        entries = [
            {
                "label": "custom-a",
                "seed": 41,
                "masses": [1.0, 1.0, 1.0],
                "ic13_mode": "zero",
            },
            {
                "label": "custom-b",
                "seed": 7,
                "masses": [1.0, 0.8, 0.6],
                "ic13_mode": "random_tanh",
            },
        ]
        config_path.write_text(json.dumps(entries), encoding="utf-8")
        completed = self._run_cli(root, "--cases-config", str(config_path))
        self.assertEqual(completed.returncode, 0, completed.stderr)
        raw = self._only_raw(root)
        self.assertEqual(len(raw["cases"]), 2)
        for recorded, expected in zip(raw["cases"], entries):
            self.assertEqual(recorded["label"], expected["label"])
            self.assertEqual(recorded["seed"], expected["seed"])
            self.assertEqual(list(recorded["masses"]), expected["masses"])
            self.assertEqual(recorded["ic13_mode"], expected["ic13_mode"])

    def test_cli_writes_provenance_evidence(self):
        probe = _load_probe()
        root = self._evidence_root("provenance")
        extra = ("--n-col", "16")
        completed = self._run_cli(root, *extra)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        raw = self._only_raw(root)
        self.assertEqual(set(raw), probe.EVIDENCE_TOP_LEVEL_KEYS)
        provenance = raw["provenance"]
        for key in (
            "argv",
            "command",
            "git_sha",
            "git_available",
            "git_worktree_dirty",
            "git_worktree_dirty_available",
            "torch_version",
            "numpy_version",
            "timestamp",
            "median_convention",
            "ic13_rng_scheme",
            "causal_clip_facts",
        ):
            self.assertIn(key, provenance)
        expected_argv = [*extra, "--evidence-root", str(root)]
        self.assertEqual(provenance["argv"], expected_argv)

    def test_cli_allocates_non_overwriting_run_dirs(self):
        _load_probe()
        root = self._evidence_root("non-overwrite")
        first = self._run_cli(root)
        second = self._run_cli(root)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        raw_paths = sorted(root.glob("*/raw.json"))
        self.assertEqual(len(raw_paths), 2)
        self.assertTrue(all(path.is_relative_to(self.tmp) for path in raw_paths))
        for path in raw_paths:
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertIn("cases", payload)
            self.assertTrue((path.parent / "summary.md").is_file())

    def test_evidence_root_inside_simulation_data_is_rejected(self):
        probe = _load_probe()
        target = ROOT / "simulation_data" / "p55-cli-reject"
        with self.assertRaises(ValueError) as raised:
            probe._reject_dataset_evidence_root(target)
        self.assertIn("simulation_data", str(raised.exception))
        code = probe.main(["--evidence-root", str(target)])
        self.assertNotEqual(code, 0)
        self.assertFalse(target.exists())

    def test_cli_exit_code_is_not_a_recipe_verdict(self):
        probe = _load_probe()
        root = self._evidence_root("completed")
        code = probe.main(["--evidence-root", str(root)])
        self.assertEqual(code, 0)
        raw = self._only_raw(root)
        self.assertEqual(set(raw), probe.EVIDENCE_TOP_LEVEL_KEYS)
        self.assertIsNone(raw["failure"])

        failed_root = self._evidence_root("failed")
        with mock.patch.object(probe, "measure_case", side_effect=RuntimeError("boom")):
            failed_code = probe.main(["--evidence-root", str(failed_root)])
        self.assertNotEqual(failed_code, 0)
        failed_raw = self._only_raw(failed_root)
        self.assertEqual(set(failed_raw), probe.EVIDENCE_TOP_LEVEL_KEYS)
        self.assertIsNotNone(failed_raw["failure"])
        self.assertEqual(failed_raw["failure"]["type"], "RuntimeError")
        self.assertIn("boom", failed_raw["failure"]["message"])


def test_stratified_bins_synthetic():
    """Ratified 16-bin / 256-per-bin structure on synthetic draws only (D-03)."""
    from pinn.constants import T_CHARACTERISTIC_TIME

    probe = _load_probe()
    rng = np.random.default_rng(0)
    times, bin_index = probe.stratified_collocation_times(rng=rng)

    assert times.shape == (probe.RATIFIED_TOTAL,)
    assert bin_index.shape == (probe.RATIFIED_TOTAL,)
    assert times.size == 4096
    assert np.bincount(bin_index, minlength=16).tolist() == [256] * 16
    assert bool(np.all(np.diff(times) >= 0))

    t_max = T_CHARACTERISTIC_TIME
    n_bins = 16
    for bin_id in range(n_bins):
        members = times[bin_index == bin_id]
        assert members.size == 256
        lo = (bin_id / n_bins) * t_max
        hi = ((bin_id + 1) / n_bins) * t_max
        if bin_id < n_bins - 1:
            assert np.all(members >= lo)
            assert np.all(members < hi)
        else:
            assert np.all(members >= lo)
            assert np.all(members <= t_max)

    first_times, first_bins = probe.stratified_collocation_times(
        rng=np.random.default_rng(0),
    )
    second_times, second_bins = probe.stratified_collocation_times(
        rng=np.random.default_rng(0),
    )
    assert np.array_equal(first_times, second_times)
    assert np.array_equal(first_bins, second_bins)

    global_before = np.random.get_state()
    probe.stratified_collocation_times(rng=np.random.default_rng(1))
    global_after = np.random.get_state()
    assert global_before[0] == global_after[0]
    assert np.array_equal(global_before[1], global_after[1])
    assert global_before[2:] == global_after[2:]

    with pytest.raises(TypeError, match="Generator"):
        probe.stratified_collocation_times(rng=0)
    with pytest.raises(ValueError, match="n_bins"):
        probe.stratified_collocation_times(n_bins=0, rng=np.random.default_rng(0))
    with pytest.raises(ValueError, match="per_bin"):
        probe.stratified_collocation_times(per_bin=0, rng=np.random.default_rng(0))


def test_bin_mean_residuals_synthetic():
    """Arithmetic bin means against a closed-form synthetic residual (D-03)."""
    probe = _load_probe()
    assignment = np.repeat(np.arange(16), 256)
    residuals = np.arange(4096, dtype=float)
    means = probe.bin_mean_residuals(residuals, assignment, n_bins=16)

    expected = 256 * np.arange(16) + 127.5
    assert means.shape == (16,)
    assert np.array_equal(means, expected)

    with pytest.raises(ValueError, match="length"):
        probe.bin_mean_residuals(residuals[:10], assignment)
    with pytest.raises(ValueError, match="bin index"):
        bad_range = assignment.copy()
        bad_range[0] = 16
        probe.bin_mean_residuals(residuals, bad_range)
    with pytest.raises(ValueError, match="empty bin"):
        probe.bin_mean_residuals(residuals, np.zeros(4096, dtype=int))


def _probe_call_graph_closure():
    """AST call-graph from run_sweep/measure_case/main, including defaults."""
    probe = _load_probe()
    tree = ast.parse(
        pathlib.Path(probe.__file__).read_text(encoding="utf-8"),
        filename=probe.__file__,
    )
    functions = {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }

    def names_in(node) -> set[str]:
        found: set[str] = set()
        if node is None:
            return found
        for child in ast.walk(node):
            if isinstance(child, ast.Name):
                found.add(child.id)
        return found

    def called_from(fn_node) -> set[str]:
        names: set[str] = set()
        roots = list(fn_node.body)
        roots.extend(fn_node.args.defaults)
        roots.extend(d for d in fn_node.args.kw_defaults if d is not None)
        for root in roots:
            for child in ast.walk(root):
                if not isinstance(child, ast.Call):
                    continue
                callee = child.func
                if isinstance(callee, ast.Name):
                    names.add(callee.id)
                elif isinstance(callee, ast.Attribute):
                    names.add(callee.attr)
        return names

    seed: set[str] = {"run_sweep", "measure_case", "main"}
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Expr)):
            seed |= names_in(node)
    for entry_name in ("run_sweep", "measure_case", "main"):
        fn_node = functions[entry_name]
        for default in fn_node.args.defaults:
            seed |= names_in(default)
        for default in fn_node.args.kw_defaults:
            seed |= names_in(default)

    reachable: set[str] = set()
    closure: set[str] = set(seed)
    stack = list(seed)
    while stack:
        name = stack.pop()
        if name in reachable or name not in functions:
            continue
        reachable.add(name)
        called = called_from(functions[name])
        closure |= called
        stack.extend(called)
    return probe, reachable, closure


def test_new_structure_helpers_unreachable_from_default_sweep():
    """D-03: default measurement path must not reach the 4096-bin helpers."""
    _probe, reachable, closure = _probe_call_graph_closure()
    assert reachable, "call-graph closure is empty — parser would green a vacuous gate"
    assert "_ic13_for_case" in reachable, (
        "known-reachable helper _ic13_for_case missing from the closure; "
        "a broken parser cannot satisfy D-03 by finding nothing"
    )
    forbidden = ("stratified_collocation_times", "bin_mean_residuals")
    leaked = [name for name in forbidden if name in closure or name in reachable]
    assert not leaked, (
        "CONTEXT.md D-03: new-structure helpers must stay unreachable from "
        f"run_sweep/measure_case/main; leaked {leaked}. Wiring them into a "
        "real measurement is Phase 56's requirement, not Phase 55's."
    )


def test_default_sweep_never_exceeds_sixteen_causal_points(tmp_path):
    """Default path must feed causal_physics_loss exactly DEFAULT_N_COL residuals."""
    probe = _load_probe()
    recorded: list[int] = []
    original = probe.causal_physics_loss

    def recorder(residuals_per_time, *args, **kwargs):
        if torch.is_tensor(residuals_per_time):
            count = int(residuals_per_time.reshape(-1).numel())
        else:
            count = int(np.asarray(residuals_per_time).reshape(-1).size)
        recorded.append(count)
        return original(residuals_per_time, *args, **kwargs)

    evidence_root = tmp_path / "evidence"
    with mock.patch.object(probe, "causal_physics_loss", side_effect=recorder):
        probe.run_sweep()
        code = probe.main(["--evidence-root", str(evidence_root)])
    assert recorded, "expected at least one causal_physics_loss call"
    assert all(count == probe.DEFAULT_N_COL for count in recorded), (
        f"default path passed residual counts {recorded} to causal_physics_loss; "
        f"every call must receive exactly DEFAULT_N_COL={probe.DEFAULT_N_COL}"
    )
    assert code == 0


def test_exact_value_fixture(default_sweep):
    _probe, results = default_sweep
    fixture = _load_fixture()
    expected_cases = fixture["cases"]
    assert [case["label"] for case in expected_cases] == [item.label for item in results]
    rel = fixture["_meta"]["relative_tolerance"]
    for result, expected in zip(results, expected_cases):
        _compare_case_to_fixture(result, expected, rel)


def test_fixture_comparison_fails_on_a_perturbed_baseline(default_sweep):
    _probe, results = default_sweep
    fixture = _load_fixture()
    perturbed = copy.deepcopy(fixture)
    perturbed["cases"][0]["rbar_median"] *= 1.01
    rel = fixture["_meta"]["relative_tolerance"]
    with pytest.raises(AssertionError):
        _compare_case_to_fixture(results[0], perturbed["cases"][0], rel)


def test_fixture_file_is_never_written_by_the_suite(default_sweep):
    _probe, results = default_sweep
    before = hashlib.sha256(FIXTURE_PATH.read_bytes()).hexdigest()
    fixture = _load_fixture()
    perturbed = copy.deepcopy(fixture)
    perturbed["cases"][0]["rbar_median"] *= 1.01
    rel = fixture["_meta"]["relative_tolerance"]
    with pytest.raises(AssertionError):
        _compare_case_to_fixture(results[0], perturbed["cases"][0], rel)
    after = hashlib.sha256(FIXTURE_PATH.read_bytes()).hexdigest()
    assert after == before
