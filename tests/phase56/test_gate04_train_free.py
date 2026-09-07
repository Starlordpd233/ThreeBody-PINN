"""Contract tests for the Phase 56 GATE-04 train-free gate (condition (i) path).

The public surface under test was frozen by the plan 56-01 Task 1 decision
checkpoint (owner answer "confirmed", 2026-09-06): the probe helper
``ratified_causal_weights``, the gate module's verdict dataclasses and single
verdict function, and the persisted ``r_ref_stage0.json`` schema.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import math
import pathlib
import shutil
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
MODULE = "pinn.verification.gate04_train_free"
PROBE_MODULE = "pinn.verification.architecture_characterization_probe"
FROZEN_TOP_LEVEL_KEYS = frozenset({
    "schema_version",
    "r_ref",
    "statistic",
    "statistic_convention",
    "cases",
    "raw_bin_means",
    "configuration",
    "provenance",
    "invalidation_triggers",
    "valid",
})
# SC5 demonstration fixture (56-03 Task 1): the pre-amendment recipe's
# recorded, known-degenerate six-case output. A second, independent fixture
# path from the RatifiedCausalWeightsTests/Gate04VerdictTests suite above,
# each protected by its own SHA-256 integrity guard.
PRE_AMENDMENT_FIXTURE_PATH = (
    pathlib.Path(__file__).resolve().parent / "fixtures" / "pre_amendment_baseline.json"
)


def _load_gate():
    """Defer production import so the RED suite skips before the module exists."""
    try:
        return importlib.import_module(MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{MODULE} has not landed yet: {exc}") from exc


def _load_ratified_weights():
    """Fail (never skip) while the probe helper is absent — the RED target.

    The probe module itself is committed (Phase 55); the planned behaviour is a
    NEW public function on it. Its absence must read as a failing assertion for
    the planned behaviour, so the RED suite proves it can go red on this seam.
    """
    probe = importlib.import_module(PROBE_MODULE)
    try:
        return probe.ratified_causal_weights
    except AttributeError as exc:
        raise AssertionError(
            f"ratified_causal_weights has not landed yet in {PROBE_MODULE} "
            "(56-01 Task 2 step 3)"
        ) from exc


def _load_pre_amendment_fixture():
    """Load the committed SC5 fixture (56-03 Task 1) — never regenerated here."""
    with PRE_AMENDMENT_FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _clip_floor():
    facts = resolve_causal_clip_facts(torch.float64, torch.device("cpu"))
    return float(facts["causal_clip_min_weight"])


def _graded_weights():
    """A healthy 16-entry weight vector (w_1 = 1, strictly graded, above the floor)."""
    return tuple(math.exp(-index) for index in range(16))


def _synthetic_case(gate, *, label="synthetic", seed=999, raw=None, r_tilde=None,
                    weights=None, min_weight=None, condition_i_satisfied=None,
                    front_idx=0):
    """Build a Gate04CaseResult directly — the verdict must audit values, not trust flags."""
    floor = _clip_floor()
    raw = tuple(1.0 for _ in range(16)) if raw is None else tuple(raw)
    r_tilde = tuple(1.0 for _ in range(16)) if r_tilde is None else tuple(r_tilde)
    weights = _graded_weights() if weights is None else tuple(weights)
    if min_weight is None:
        finite = [w for w in weights if math.isfinite(w)]
        min_weight = min(finite) if finite else float("nan")
    if condition_i_satisfied is None:
        condition_i_satisfied = all(math.isfinite(w) and w > floor for w in weights)
    return gate.Gate04CaseResult(
        label=label,
        seed=seed,
        raw_bin_means=raw,
        r_tilde=r_tilde,
        weights=weights,
        front_idx=front_idx,
        min_weight=min_weight,
        condition_i_satisfied=condition_i_satisfied,
        condition_ii_diagnostics=None,
        condition_iii_diagnostics=None,
    )


@pytest.fixture(scope="session", autouse=True)
def _assert_pre_amendment_baseline_sha256_unchanged():
    """SC5 integrity guard (56-03 Task 2) — separate from any guard 56-01 or
    56-02 added, protecting this specific committed fixture only."""
    digest = hashlib.sha256(PRE_AMENDMENT_FIXTURE_PATH.read_bytes()).hexdigest()
    yield
    assert hashlib.sha256(PRE_AMENDMENT_FIXTURE_PATH.read_bytes()).hexdigest() == digest, (
        "tests/phase56/fixtures/pre_amendment_baseline.json was rewritten during "
        "the suite; the SC5 demonstration baseline must never heal itself"
    )


class RatifiedCausalWeightsTests(unittest.TestCase):
    """The D-05 probe helper: ratified-recipe weights via the trainer's own loss."""

    def test_flat_profile_matches_exclusive_prefix(self):
        ratified_causal_weights = _load_ratified_weights()
        raw = np.full(16, 3.5, dtype=np.float64)
        weights = ratified_causal_weights(
            raw, 3.5, dtype=torch.float64, device=torch.device("cpu"),
        )
        expected = np.exp(-np.arange(16, dtype=np.float64))
        assert isinstance(weights, np.ndarray)
        assert weights.shape == (16,)
        assert weights.dtype == np.float64
        # The exclusive prefix of bin 0 is empty, so w_1 = exp(0) = 1 exactly.
        assert weights[0] == 1.0
        assert bool(np.all(np.diff(weights) < 0.0)), "weights must strictly decrease"
        np.testing.assert_allclose(weights, expected, rtol=1e-12, atol=0.0)

    def test_rejects_wrong_length(self):
        ratified_causal_weights = _load_ratified_weights()
        for length in (0, 15, 17):
            with self.subTest(length=length):
                with pytest.raises(ValueError, match="raw_bin_means"):
                    ratified_causal_weights(
                        np.ones(length), 1.0,
                        dtype=torch.float64, device=torch.device("cpu"),
                    )

    def test_rejects_bad_r_ref(self):
        ratified_causal_weights = _load_ratified_weights()
        for bad in (0.0, -1.0, float("nan"), float("inf")):
            with self.subTest(r_ref=bad):
                with pytest.raises(ValueError, match="r_ref"):
                    ratified_causal_weights(
                        np.ones(16), bad,
                        dtype=torch.float64, device=torch.device("cpu"),
                    )

    def test_rejects_non_finite_entry(self):
        ratified_causal_weights = _load_ratified_weights()
        for bad in (float("nan"), float("inf"), float("-inf")):
            raw = np.ones(16, dtype=np.float64)
            raw[7] = bad
            with self.subTest(entry=bad):
                with pytest.raises(ValueError, match="raw_bin_means"):
                    ratified_causal_weights(
                        raw, 2.0,
                        dtype=torch.float64, device=torch.device("cpu"),
                    )


class Gate04VerdictTests(unittest.TestCase):
    """gate04_verdict is the single source of the PASS/BLOCK decision."""

    def test_strict_floor_boundary_blocks_and_passes(self):
        gate = _load_gate()
        floor = _clip_floor()
        weights = list(_graded_weights())
        weights[11] = floor  # exactly AT the floor: pinned by definition
        pinned = _synthetic_case(gate, weights=weights)
        assert gate.gate04_verdict([pinned], causal_clip_min_weight=floor) == gate.VERDICT_BLOCK

        weights[11] = float(np.nextafter(floor, math.inf))  # strictly above the floor
        cleared = _synthetic_case(gate, weights=weights)
        assert gate.gate04_verdict([cleared], causal_clip_min_weight=floor) == gate.VERDICT_PASS

    def test_blocks_non_finite_entries(self):
        gate = _load_gate()
        floor = _clip_floor()
        nan_residual = [1.0] * 16
        nan_residual[3] = float("nan")
        huge = [1e308] * 16  # finite entries whose exclusive prefix overflows
        inf_weights = list(_graded_weights())
        inf_weights[5] = float("inf")
        variants = {
            "residual": _synthetic_case(gate, raw=nan_residual),
            "prefix": _synthetic_case(gate, r_tilde=huge),
            "weights": _synthetic_case(gate, weights=inf_weights),
        }
        for name, case in variants.items():
            with self.subTest(non_finite=name):
                assert gate.gate04_verdict([case], causal_clip_min_weight=floor) == gate.VERDICT_BLOCK

    def test_non_finite_reason_named_in_verdict_object(self):
        gate = _load_gate()
        weights = list(_graded_weights())
        weights[9] = float("nan")
        bad = _synthetic_case(gate, label="41", seed=41, weights=weights)
        with mock.patch.object(gate, "compute_r_ref", return_value=(2.0, (bad.raw_bin_means,))), \
             mock.patch.object(gate, "evaluate_case", return_value=bad):
            verdict = gate.run_gate(cases=gate.DEFAULT_CASES[:1], precision="float64", device="cpu")
        assert verdict.verdict == gate.VERDICT_BLOCK
        assert any(
            "non-finite" in reason and "weights" in reason
            for reason in verdict.blocking_reasons
        ), verdict.blocking_reasons

    def test_empty_case_set_blocks(self):
        gate = _load_gate()
        floor = _clip_floor()
        assert gate.gate04_verdict([], causal_clip_min_weight=floor) == gate.VERDICT_BLOCK
        verdict = gate.run_gate(cases=(), precision="float64", device="cpu")
        assert verdict.verdict == gate.VERDICT_BLOCK
        assert verdict.cases == ()
        assert any("empty" in reason for reason in verdict.blocking_reasons)

    def test_blocks_when_front_index_uncomputable_from_non_finite_weight(self):
        """Condition (iii)'s finiteness tie (56-02 D-06): a front index derived
        from a weight vector containing a non-finite entry cannot be trusted
        as a capability signal, so GATE-04 blocks even though ``_front_idx``
        itself never raises on a NaN entry (NaN fails every ``> 0.5``
        comparison and is silently excluded from the max, rather than
        detected as an error) — the actual protection is condition (i)'s
        existing finiteness rule over the weight vector."""
        gate = _load_gate()
        floor = _clip_floor()
        weights = list(_graded_weights())
        weights[6] = float("nan")
        front_idx = gate._front_idx(weights)
        case = _synthetic_case(gate, weights=weights, front_idx=front_idx)
        assert gate.gate04_verdict([case], causal_clip_min_weight=floor) == gate.VERDICT_BLOCK


class RunGateEndToEndTests(unittest.TestCase):
    """The tracer slice: the six audited cases through the ratified recipe."""

    def test_run_gate_six_default_cases_pass(self):
        gate = _load_gate()
        floor = _clip_floor()
        verdict = gate.run_gate()
        assert verdict.verdict == gate.VERDICT_PASS, verdict.blocking_reasons
        assert verdict.blocking_reasons == ()
        # 56-02 Task 1: condition (iii)'s capability structure is now wired
        # with its grounded fail-closed rule; only condition (ii) remains
        # unratified (GAP-56-01).
        assert verdict.unratified_conditions == ("ii",)
        assert [case.label for case in verdict.cases] == [case.label for case in gate.DEFAULT_CASES]
        for case in verdict.cases:
            assert len(case.raw_bin_means) == 16
            assert len(case.r_tilde) == 16
            assert len(case.weights) == 16
            assert case.min_weight > verdict.causal_clip_min_weight
            assert case.condition_i_satisfied is True
            cond_ii = case.condition_ii_diagnostics
            assert cond_ii is not None and cond_ii["status"] == "UNRATIFIED", cond_ii
            cond_iii = case.condition_iii_diagnostics
            assert cond_iii is not None and cond_iii["status"] == "UNRATIFIED", cond_iii
            # 56-RESEARCH.md Pitfall 3 / b.3: front_idx == 0 at init is the
            # EXPECTED, healthy result for every one of the six cases — never
            # a failure signal. A fixed positive-front check would reject
            # every case in this loop.
            assert cond_iii["unperturbed_front_idx"] == 0, (case.label, cond_iii)
            # Pitfall 4 / b.5: a reduction confined to bins 8-15 cannot move
            # front_idx at any magnitude — the whole response series must sit
            # constant at the unperturbed value.
            assert set(cond_iii["late_bin_only_response_front_idx"]) == {0}, (
                case.label, cond_iii["late_bin_only_response_front_idx"],
            )
            # b.4: front_idx must never DECREASE as the uniform factor shrinks
            # (CONDITION_III_DIAGNOSTIC_FACTORS is ordered 1.0 -> 0.001).
            uniform = cond_iii["uniform_response_front_idx"]
            assert all(a <= b for a, b in zip(uniform, uniform[1:])), (case.label, uniform)
        assert verdict.causal_clip_min_weight == floor
        assert math.isfinite(verdict.r_ref) and verdict.r_ref > 0.0
        all_means = np.concatenate([np.asarray(case.raw_bin_means) for case in verdict.cases])
        assert all_means.size == 96
        assert math.isclose(
            verdict.r_ref, float(np.median(all_means)), rel_tol=1e-12, abs_tol=0.0,
        )


class ConditionIIUnratifiedSlotTests(unittest.TestCase):
    """GAP-56-01: condition (ii) is structurally present, measurable, and
    impossible to satisfy or fail without an owner ruling."""

    def test_condition_ii_verdict_raises_not_implemented(self):
        gate = _load_gate()
        with pytest.raises(NotImplementedError, match="GAP-56-01"):
            gate.condition_ii_verdict(_graded_weights())

    def test_condition_ii_verdict_raises_for_every_input(self):
        gate = _load_gate()
        for bad in (None, [], "not-a-vector", [float("nan")] * 16, list(_graded_weights())):
            with self.subTest(weights=bad):
                with pytest.raises(NotImplementedError, match="GAP-56-01"):
                    gate.condition_ii_verdict(bad)

    def test_condition_ii_diagnostics_returns_exact_key_set(self):
        gate = _load_gate()
        floor = _clip_floor()
        diag = gate.condition_ii_diagnostics(_graded_weights(), floor)
        assert set(diag) == {
            "coefficient_of_variation_tail",
            "monotone_non_increasing",
            "dynamic_range_decades",
            "distinct_non_floor_count",
            "status",
        }
        assert diag["status"] == "UNRATIFIED"
        assert diag["monotone_non_increasing"] is True
        assert isinstance(diag["coefficient_of_variation_tail"], float)
        assert isinstance(diag["dynamic_range_decades"], float)
        assert isinstance(diag["distinct_non_floor_count"], int)
        # _graded_weights() clears the dtype floor at every one of 16 entries.
        assert diag["distinct_non_floor_count"] == 16

    def test_condition_ii_diagnostics_carries_no_verdict_shaped_field(self):
        gate = _load_gate()
        floor = _clip_floor()
        diag = gate.condition_ii_diagnostics(_graded_weights(), floor)
        forbidden = ("threshold", "passed", "satisfied", "ok")
        for key in diag:
            lowered = key.lower()
            for word in forbidden:
                assert word not in lowered, (key, word)

    def test_condition_ii_diagnostics_rejects_wrong_length(self):
        gate = _load_gate()
        floor = _clip_floor()
        for length in (0, 15, 17):
            with self.subTest(length=length):
                with pytest.raises(ValueError, match="16"):
                    gate.condition_ii_diagnostics([1.0] * length, floor)


class ConditionIIIDiagnosticsStructureTests(unittest.TestCase):
    """Condition (iii)'s capability record: structure and no-threshold checks
    on synthetic data. The REAL six-case physical behaviour (universal zero
    front index; late-bin-only non-response; monotone uniform response) is
    asserted in RunGateEndToEndTests, reusing that test's own run_gate()
    measurement rather than paying for a second one here."""

    @staticmethod
    def _synthetic_raw_means():
        # Illustrative only: this class proves the RECORD'S STRUCTURE, not
        # the ratified recipe's real physical behaviour.
        return np.linspace(1.0e10, 2.0e10, 16)

    def test_returns_exact_key_set_and_unratified_status(self):
        gate = _load_gate()
        diag = gate.condition_iii_diagnostics(
            self._synthetic_raw_means(), 1.5e10,
            dtype=torch.float64, device=torch.device("cpu"),
        )
        assert set(diag) == {
            "factors",
            "late_bin_start",
            "unperturbed_front_idx",
            "uniform_response_front_idx",
            "late_bin_only_response_front_idx",
            "status",
        }
        assert diag["status"] == "UNRATIFIED"
        assert diag["late_bin_start"] == 8
        assert len(diag["uniform_response_front_idx"]) == len(diag["factors"])
        assert len(diag["late_bin_only_response_front_idx"]) == len(diag["factors"])

    def test_carries_no_verdict_shaped_field(self):
        gate = _load_gate()
        diag = gate.condition_iii_diagnostics(
            self._synthetic_raw_means(), 1.5e10,
            dtype=torch.float64, device=torch.device("cpu"),
        )
        forbidden = ("threshold", "passed", "satisfied", "ok")
        for key in diag:
            lowered = key.lower()
            for word in forbidden:
                assert word not in lowered, (key, word)

    def test_uses_default_factors_constant(self):
        gate = _load_gate()
        assert gate.CONDITION_III_DIAGNOSTIC_FACTORS[0] == 1.0
        assert gate.CONDITION_III_DIAGNOSTIC_FACTORS[-1] < 0.01
        diag = gate.condition_iii_diagnostics(
            self._synthetic_raw_means(), 1.5e10,
            dtype=torch.float64, device=torch.device("cpu"),
        )
        assert tuple(diag["factors"]) == gate.CONDITION_III_DIAGNOSTIC_FACTORS

    def test_docstring_states_both_structural_findings(self):
        gate = _load_gate()
        doc = gate.condition_iii_diagnostics.__doc__ or ""
        assert "front index of 0" in doc
        assert "exclusive prefix" in doc

    def test_rejects_wrong_length(self):
        gate = _load_gate()
        for length in (0, 15, 17):
            with self.subTest(length=length):
                with pytest.raises(ValueError, match="16"):
                    gate.condition_iii_diagnostics(
                        [1.0] * length, 1.5e10,
                        dtype=torch.float64, device=torch.device("cpu"),
                    )


class RRefArtifactTests(unittest.TestCase):
    """The persisted R_ref artifact carries the frozen schema, written atomically."""

    def _synthetic_verdict(self, gate):
        floor = _clip_floor()
        cases = tuple(
            _synthetic_case(
                gate, label=case.label, seed=case.seed,
                raw=[2.0] * 16, r_tilde=[1.0] * 16,
            )
            for case in gate.DEFAULT_CASES
        )
        return gate.Gate04Verdict(
            verdict=gate.VERDICT_PASS,
            blocking_reasons=(),
            unratified_conditions=("ii", "iii"),
            cases=cases,
            r_ref=2.0,
            causal_clip_min_weight=floor,
            precision="float64",
            device="cpu",
        )

    def test_write_r_ref_artifact_frozen_schema(self):
        gate = _load_gate()
        verdict = self._synthetic_verdict(gate)
        with tempfile.TemporaryDirectory(prefix="phase56-rref-") as tmp:
            path = pathlib.Path(tmp) / "nested" / "r_ref_stage0.json"
            written = gate.write_r_ref_artifact(verdict, path=path)
            assert written == path
            payload = json.loads(path.read_text(encoding="utf-8"))
            assert set(payload) == FROZEN_TOP_LEVEL_KEYS, sorted(payload)
            assert payload["schema_version"] == "phase56-r-ref-stage0/v1"
            assert payload["schema_version"] == gate.R_REF_SCHEMA_VERSION
            assert payload["r_ref"] == 2.0
            assert payload["statistic"] == "median"
            assert payload["statistic_convention"]
            assert [entry["label"] for entry in payload["cases"]] == [
                case.label for case in gate.DEFAULT_CASES
            ]
            assert len(payload["raw_bin_means"]) == 6
            assert all(len(row) == 16 for row in payload["raw_bin_means"])
            assert all(
                all(math.isfinite(value) for value in row)
                for row in payload["raw_bin_means"]
            )
            assert len(payload["invalidation_triggers"]) > 0
            assert payload["valid"] is True
            assert payload["configuration"]["precision"] == "float64"
            assert payload["configuration"]["device"] == "cpu"
            assert not list(pathlib.Path(tmp).rglob("*.tmp.*")), (
                "the atomic writer must leave no temp residue"
            )


class PublicContractTests(unittest.TestCase):
    """The Task-1-frozen names Phase 57 imports (owner answer: "confirmed")."""

    def test_probe_helper_exported(self):
        probe = importlib.import_module(PROBE_MODULE)
        assert "ratified_causal_weights" in probe.__all__

    def test_gate_public_surface(self):
        gate = _load_gate()
        assert gate.VERDICT_PASS == "PASS"
        assert gate.VERDICT_BLOCK == "BLOCK"
        for name in (
            "Gate04Verdict",
            "Gate04CaseResult",
            "gate04_verdict",
            "run_gate",
            "write_r_ref_artifact",
            "compute_r_ref",
            "evaluate_case",
            "R_REF_SCHEMA_VERSION",
            "R_REF_ARTIFACT_PATH",
            "INVALIDATION_TRIGGERS",
            "condition_ii_verdict",
            "condition_ii_diagnostics",
            "condition_iii_diagnostics",
            "CONDITION_III_DIAGNOSTIC_FACTORS",
            "main",
            "EVIDENCE_SCHEMA_VERSION",
            "EVIDENCE_TOP_LEVEL_KEYS",
        ):
            assert hasattr(gate, name), name
        assert gate.R_REF_ARTIFACT_PATH.name == "r_ref_stage0.json"
        assert gate.R_REF_ARTIFACT_PATH.parent.name == "artifacts"


class Gate04CLIDefaultRunTests(unittest.TestCase):
    """One real, no-argument CLI invocation proves the zero-argument
    contract, provenance completeness, and the printed verdict/INCOMPLETE
    line together — a shared ``setUpClass`` run so the ~200s six-case
    measurement is paid once, not once per assertion group."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory(prefix="phase56-gate04-cli-default-")
        cls.tmp = pathlib.Path(cls._tmp.name)
        cls.evidence_root = cls.tmp / "evidence" / "default"
        cls.completed = subprocess.run(
            [sys.executable, "-m", MODULE, "--evidence-root", str(cls.evidence_root)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        cls.raw_paths = (
            sorted(cls.evidence_root.glob("*/raw.json"))
            if cls.evidence_root.is_dir()
            else []
        )
        cls.raw = (
            json.loads(cls.raw_paths[0].read_text(encoding="utf-8"))
            if len(cls.raw_paths) == 1
            else None
        )

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_exits_zero(self):
        assert self.completed.returncode == 0, self.completed.stderr

    def test_writes_exactly_one_evidence_directory_with_six_default_labels_in_order(self):
        gate = _load_gate()
        assert len(self.raw_paths) == 1, self.raw_paths
        assert self.raw is not None
        assert [c["label"] for c in self.raw["cases"]] == [
            c.label for c in gate.DEFAULT_CASES
        ]

    def test_frozen_top_level_key_set(self):
        gate = _load_gate()
        assert self.raw is not None
        assert set(self.raw) == gate.EVIDENCE_TOP_LEVEL_KEYS, sorted(self.raw)
        assert self.raw["failure"] is None

    def test_provenance_block_complete(self):
        assert self.raw is not None
        provenance = self.raw["provenance"]
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
        ):
            assert key in provenance, key

    def test_printed_summary_names_verdict_and_incomplete_token(self):
        stdout = self.completed.stdout
        assert "verdict=" in stdout, stdout
        # GAP-56-01 is OPEN: unratified_conditions is non-empty, so a PASS
        # must never read as a complete GATE-04 clearance.
        assert "INCOMPLETE" in stdout, stdout
        assert "GAP-56-01" in stdout, stdout
        assert any(line.startswith("evidence=") for line in stdout.splitlines()), stdout


class Gate04CLIEvidenceDirectoryTests(unittest.TestCase):
    """Non-overwriting evidence directories, proven with a minimal 1-case
    config so the collision test does not pay the six-case measurement cost
    twice."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="phase56-gate04-evdir-")
        self.addCleanup(self._tmp.cleanup)
        self.tmp = pathlib.Path(self._tmp.name)

    def _one_case_config(self) -> pathlib.Path:
        path = self.tmp / "one-case.json"
        path.write_text(
            json.dumps(
                [{"label": "single", "seed": 41, "masses": [1.0, 1.0, 1.0], "ic13_mode": "zero"}]
            ),
            encoding="utf-8",
        )
        return path

    def test_two_runs_allocate_distinct_directories(self):
        root = self.tmp / "evidence"
        config = self._one_case_config()
        for _ in range(2):
            completed = subprocess.run(
                [sys.executable, "-m", MODULE, "--cases-config", str(config),
                 "--evidence-root", str(root)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            assert completed.returncode == 0, completed.stderr
        run_dirs = [p for p in root.iterdir() if p.is_dir()]
        assert len(run_dirs) == 2, run_dirs


class Gate04CLIFailureModeTests(unittest.TestCase):
    """Malformed input and a hostile evidence root fail closed, cheaply
    (before any six-case measurement is attempted)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="phase56-gate04-fail-")
        self.addCleanup(self._tmp.cleanup)
        self.tmp = pathlib.Path(self._tmp.name)

    def test_malformed_json_cases_config_fails_closed(self):
        config = self.tmp / "bad.json"
        config.write_text("{not valid json", encoding="utf-8")
        root = self.tmp / "evidence"
        completed = subprocess.run(
            [sys.executable, "-m", MODULE, "--cases-config", str(config),
             "--evidence-root", str(root)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        assert completed.returncode != 0, completed.stdout
        raw_paths = sorted(root.glob("*/raw.json"))
        assert len(raw_paths) == 1, raw_paths
        raw = json.loads(raw_paths[0].read_text(encoding="utf-8"))
        assert raw["failure"] is not None
        assert raw["verdict"] != "PASS"

    def test_unknown_ic13_mode_fails_closed(self):
        config = self.tmp / "bad_mode.json"
        config.write_text(
            json.dumps([{"label": "x", "seed": 1, "masses": [1.0, 1.0, 1.0], "ic13_mode": "bogus"}]),
            encoding="utf-8",
        )
        root = self.tmp / "evidence"
        completed = subprocess.run(
            [sys.executable, "-m", MODULE, "--cases-config", str(config),
             "--evidence-root", str(root)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        assert completed.returncode != 0, completed.stdout
        raw_paths = sorted(root.glob("*/raw.json"))
        assert len(raw_paths) == 1, raw_paths
        raw = json.loads(raw_paths[0].read_text(encoding="utf-8"))
        assert raw["failure"] is not None
        assert raw["verdict"] != "PASS"

    def test_dataset_evidence_root_rejected_before_any_write(self):
        gate = _load_gate()
        root = ROOT / "simulation_data" / "phase56-cli-should-not-write"
        assert not root.exists(), "test precondition: path must not pre-exist"
        try:
            exit_code = gate.main(["--evidence-root", str(root)])
            assert exit_code != 0
            assert not root.exists(), "evidence root must not be created for a rejected path"
        finally:
            if root.exists():
                shutil.rmtree(root)

    def test_dataset_r_ref_path_rejected_before_any_write(self):
        gate = _load_gate()
        path = ROOT / "simulation_data" / "phase56-cli-should-not-write" / "r_ref.json"
        assert not path.parent.exists(), "test precondition: path must not pre-exist"
        try:
            exit_code = gate.main(["--r-ref-path", str(path)])
            assert exit_code != 0
            assert not path.parent.exists(), (
                "r-ref-path's parent must not be created for a rejected path"
            )
        finally:
            if path.parent.exists():
                shutil.rmtree(path.parent)


class Gate04CLINoBypassTests(unittest.TestCase):
    """The CLI adds no way to force a PASS or skip the gate (threat T-56-08/09).

    The sibling "registered in no CI/verify config" acceptance check is a
    literal repo-wide grep (56-02-PLAN.md acceptance criteria) run directly
    during verification, not duplicated here as a pytest test — a rglob over
    the whole repository is unnecessary suite weight for a check that has
    one specified, authoritative command."""

    def test_module_defines_no_bypass_vocabulary(self):
        source = pathlib.Path(
            importlib.import_module(MODULE).__file__
        ).read_text(encoding="utf-8")
        for word in ("force", "skip_gate", "allow_block", "ignore_verdict"):
            assert word not in source, word


class Gate04PreAmendmentDemonstrationTests(unittest.TestCase):
    """SC5 (ROADMAP Phase 56 success criterion 5): ``gate04_verdict`` — the
    SAME function ``run_gate`` calls for the amended recipe — BLOCKs the
    pre-amendment recipe's six recorded cases (naming condition (i) for
    every one) and PASSes the amended recipe's six live cases. Two inputs,
    one verdict function, opposite outcomes: that pairing is what makes this
    a demonstration rather than a tautology (T-56-15). No demonstration-only
    verdict path is defined in this file — every assertion below calls
    ``gate.gate04_verdict`` or ``gate._blocking_reasons``, the exact private
    audit ``gate04_verdict`` itself calls internally (mirrors how
    ``run_gate`` assembles a ``Gate04Verdict`` from those same two calls).

    Case construction reuses ``_synthetic_case`` (not a parallel builder):
    each pre-amendment case's real recorded ``causal_weights`` and
    ``front_idx`` (56-03 Task 1 fixture) are fed through the module's own
    frozen ``Gate04CaseResult`` dataclass, so the inputs travel the same
    validation path a live measurement takes. ``raw_bin_means``/``r_tilde``
    are not part of this fixture's schema (only the per-case median is) and
    play no role in condition (i)'s floor check (``_blocking_reasons`` reads
    only ``weights`` for that rule), so ``_synthetic_case``'s finite
    placeholder default is used for both, exactly as the existing
    ``Gate04VerdictTests`` floor-boundary tests already do.
    """

    @classmethod
    def setUpClass(cls):
        cls.gate = _load_gate()
        cls.floor = _clip_floor()
        fixture = _load_pre_amendment_fixture()
        cls.fixture_cases = fixture["cases"]
        assert len(cls.fixture_cases) == 6, cls.fixture_cases
        cls.pre_amendment_cases = tuple(
            _synthetic_case(
                cls.gate,
                label=entry["label"],
                seed=entry["seed"],
                weights=entry["causal_weights"],
                front_idx=entry["front_idx"],
            )
            for entry in cls.fixture_cases
        )
        # The paired positive: one real, live amended-recipe six-case run,
        # paid once for the whole class (mirrors Gate04CLIDefaultRunTests'
        # own ~200s-once-per-class amortization, not a second measurement).
        cls.amended_verdict = cls.gate.run_gate()

    def test_pre_amendment_recipe_blocks_every_case_individually(self):
        for entry, case in zip(self.fixture_cases, self.pre_amendment_cases):
            with self.subTest(label=entry["label"]):
                verdict = self.gate.gate04_verdict(
                    [case], causal_clip_min_weight=self.floor,
                )
                assert verdict == self.gate.VERDICT_BLOCK, entry["label"]

    def test_pre_amendment_recipe_blocking_reasons_name_condition_i(self):
        for entry, case in zip(self.fixture_cases, self.pre_amendment_cases):
            with self.subTest(label=entry["label"]):
                reasons = self.gate._blocking_reasons(
                    [case], causal_clip_min_weight=self.floor,
                )
                assert reasons, entry["label"]
                assert any(
                    "clamp floor" in reason and "condition (i)" in reason
                    for reason in reasons
                ), (entry["label"], reasons)

    def test_pre_amendment_recipe_blocks_all_six_at_once(self):
        verdict = self.gate.gate04_verdict(
            self.pre_amendment_cases, causal_clip_min_weight=self.floor,
        )
        assert verdict == self.gate.VERDICT_BLOCK
        reasons = self.gate._blocking_reasons(
            self.pre_amendment_cases, causal_clip_min_weight=self.floor,
        )
        # Exact "case <label!r>:" prefix match — plain substring containment
        # would let label "41" false-match inside "41-variable-mass"'s reasons.
        named = {
            entry["label"]
            for entry in self.fixture_cases
            if any(
                reason.startswith(f"case {entry['label']!r}:")
                and "condition (i)" in reason
                for reason in reasons
            )
        }
        assert named == {entry["label"] for entry in self.fixture_cases}, (named, reasons)

    def test_pre_amendment_paired_amended_recipe_passes(self):
        verdict = self.amended_verdict
        assert verdict.verdict == self.gate.VERDICT_PASS, verdict.blocking_reasons
        # Re-invoke gate04_verdict directly on the live verdict's own case
        # results: the SAME function the BLOCK assertions above call, fed the
        # amended recipe's real measured cases -- not a second, demonstration-
        # only path.
        replayed = self.gate.gate04_verdict(
            verdict.cases, causal_clip_min_weight=verdict.causal_clip_min_weight,
        )
        assert replayed == self.gate.VERDICT_PASS
