"""Phase 57 Task 2/3 — the exact GATE-04 ruling and (Task 3) the EVAL-02
canonical-frame boundary, structural candidate selection, and run-failure
classification.

Every test here drives a real production seam
(``pinn.verification.gate04_train_free``,
``pinn.verification.architecture_characterization_probe``, ``pinn.evaluate``)
or a fixed, tamper-evident, ALREADY-COMMITTED evidence artifact -- never a
re-measured network forward pass (the real six-case measurement is
several minutes of CPU/AD work, unsuitable for this focused suite; it is
exercised for real only by the separate production-path verification wave,
57-RESEARCH.md "Ordered Implementation Waves" step 4). Every test is
expected to be RED because these behaviors are not yet implemented -- never
because of an import, syntax, fixture, data, or environment error.
"""

from __future__ import annotations

import importlib
import importlib.util
import inspect
import json
import math
import tempfile
import unittest
from pathlib import Path

import torch

import pinn.evaluate as evaluate
from pinn.verification.architecture_characterization_probe import RATIFIED_N_BINS
from pinn.verification.gate04_train_free import condition_ii_verdict

_PHASE_57_DIR = Path(__file__).resolve().parents[2] / (
    ".planning/phases/57-corrected-re-run-the-preserved-evaluation"
)
_PHASE_56_EVIDENCE = (
    Path(__file__).resolve().parents[2]
    / ".planning/phases/56-contract-amendment-train-free-gate"
    / "evidence/gate04/20260907T033409Z/raw.json"
)
_PHASE_56_EVIDENCE_SHA256 = (
    "38711a5e3bd67a05a9912e09ed9258b6db91f720a69e215e0fd4effecb3db358"
)


class Gate04RulingTests(unittest.TestCase):
    """57-RULING.md §1's exact GATE-04 condition-(ii) rule.

    ``condition_ii_verdict`` currently raises ``NotImplementedError``
    UNCONDITIONALLY for every input, under its existing single-argument
    ``condition_ii_verdict(weights)`` signature (GAP-56-01, OPEN). The owner
    ruling requires the verdict to be computed FROM the raw bin means and
    the frozen ``R_ref`` (never from a static weight vector alone), because
    the controlled-reduction response must be RECOMPUTED through the real
    production arithmetic (``ratified_causal_weights`` /
    ``causal_physics_loss``) at a scaled input. This module targets the
    bounded signature ``condition_ii_verdict(raw_bin_means, r_ref, *,
    eta_c=..., dtype=..., device=..., t_max=...) -> Mapping`` returning at
    least ``{"satisfied", "baseline_spread", "alpha", "w_prime_15",
    "front_idx", "min_perturbed_weight"}``.
    """

    DTYPE = torch.float64
    DEVICE = torch.device("cpu")

    def test_baseline_non_anchor_spread_below_two_to_one_fails(self) -> None:
        """All 16 raw means near-zero -> near-flat weights -> spread ~= 1."""
        degenerate = [1e-9] * RATIFIED_N_BINS
        result = condition_ii_verdict(
            degenerate, 1.0, dtype=self.DTYPE, device=self.DEVICE,
        )
        self.assertFalse(
            result["satisfied"],
            "a weight vector whose non-anchor spread is below 2:1 must "
            "fail condition (ii) (57-RULING.md baseline non-degeneracy)",
        )
        self.assertLess(result["baseline_spread"], 2.0)

    def test_healthy_case_passes_with_the_exact_ruling_quantities(self) -> None:
        """Ground truth independently computed via ``ratified_causal_weights``
        (2026-09-08, this session): raw=[0.1]*15+[0.05], r_ref=1.0 gives
        baseline spread ~4.0552, alpha ~0.23104906018664836, and a
        controlled-reduction response of front_idx=15,
        w'_15 = min(perturbed tail) ~0.7071067811865477 ~= 1/sqrt(2).
        """
        healthy = [0.1] * 15 + [0.05]
        result = condition_ii_verdict(
            healthy, 1.0, dtype=self.DTYPE, device=self.DEVICE,
        )
        self.assertTrue(result["satisfied"])
        self.assertGreaterEqual(result["baseline_spread"], 2.0)
        self.assertAlmostEqual(result["alpha"], 0.23104906018664836, places=9)
        self.assertAlmostEqual(
            result["w_prime_15"], 1.0 / math.sqrt(2.0), places=9,
        )
        self.assertEqual(result["front_idx"], 15)
        self.assertGreaterEqual(result["min_perturbed_weight"], 0.70)
        self.assertAlmostEqual(
            result["min_perturbed_weight"], 1.0 / math.sqrt(2.0), places=9,
        )

    def test_alpha_formula_is_log2_over_two_p15(self) -> None:
        healthy = [0.2] * 15 + [0.01]
        r_ref = 2.0
        x = [v / r_ref for v in healthy]
        p15 = sum(x[:15])
        expected_alpha = math.log(2.0) / (2.0 * p15)
        result = condition_ii_verdict(
            healthy, r_ref, dtype=self.DTYPE, device=self.DEVICE,
        )
        self.assertAlmostEqual(result["alpha"], expected_alpha, places=9)

    def test_across_all_six_committed_phase_56_cases(self) -> None:
        """"across all six cases" (57-01-PLAN.md Task 2 behavior) -- using
        the REAL, already-committed, tamper-evident Phase-56 GATE-04
        evidence 57-RULING.md §4 cites and replays (fast: no network
        forward pass is re-run), reproducing 57-RULING.md §4's own table to
        the displayed precision.
        """
        if not _PHASE_56_EVIDENCE.is_file():
            self.fail(
                f"expected committed Phase-56 GATE-04 evidence at "
                f"{_PHASE_56_EVIDENCE}; 57-RULING.md §4 cites this "
                "exact file"
            )
        raw_bytes = _PHASE_56_EVIDENCE.read_bytes()
        import hashlib
        self.assertEqual(
            hashlib.sha256(raw_bytes).hexdigest(), _PHASE_56_EVIDENCE_SHA256,
            "the committed Phase-56 evidence file must be byte-identical "
            "to the one 57-RULING.md §4 recorded and replayed",
        )
        payload = json.loads(raw_bytes)
        r_ref = payload["verdict"]["r_ref"]
        expected = {
            "41": 300522.943,
            "42": 3.58556874e09,
            "43": 842942.692,
            "0": 3641741.37,
            "7": 347257.822,
            "41-variable-mass": 5617891.92,
        }
        for case in payload["cases"]:
            result = condition_ii_verdict(
                case["raw_bin_means"], r_ref, dtype=self.DTYPE, device=self.DEVICE,
            )
            self.assertTrue(
                result["satisfied"],
                f"case {case['label']!r} must satisfy condition (ii)",
            )
            self.assertAlmostEqual(
                result["baseline_spread"] / expected[case["label"]], 1.0,
                places=3,
                msg=f"case {case['label']!r} baseline spread mismatch",
            )
            self.assertEqual(result["front_idx"], 15)
            self.assertGreaterEqual(result["min_perturbed_weight"], 0.70)
            self.assertAlmostEqual(
                result["w_prime_15"], 1.0 / math.sqrt(2.0), places=6,
            )

    def test_persisted_complete_pass_and_r_ref_provenance(self) -> None:
        """RUN-04 requires a FRESH complete GATE-04 PASS on the amended
        recipe -- the historical Phase-56
        'PASS INCOMPLETE (unratified: ii)' evidence is explicitly NOT run
        authorization (57-RULING.md §5). Checks the REAL Phase-57
        raw.json and the matching governed R_ref artifact rather than
        trusting a CLI exit code of 0.
        """
        candidates = sorted(_PHASE_57_DIR.glob("evidence/gate04/*/raw.json"))
        if not candidates:
            self.fail(
                "no Phase-57 GATE-04 evidence found under "
                f"{_PHASE_57_DIR / 'evidence' / 'gate04'} -- RUN-04 requires "
                "a fresh complete GATE-04 PASS (unratified_conditions == []) "
                "on the amended recipe before any run"
            )
        latest = candidates[-1]
        payload = json.loads(latest.read_text(encoding="utf-8"))
        verdict = payload["verdict"]
        self.assertEqual(verdict["verdict"], "PASS")
        self.assertEqual(
            verdict["unratified_conditions"], [],
            "GATE-04 must be a COMPLETE PASS -- no unratified conditions",
        )
        r_ref_artifact_path = (
            Path(__file__).resolve().parents[2]
            / "pinn/verification/artifacts/r_ref_stage0.json"
        )
        artifact = json.loads(r_ref_artifact_path.read_text(encoding="utf-8"))
        self.assertTrue(artifact.get("valid"))
        self.assertEqual(artifact["r_ref"], verdict["r_ref"])


class EvaluationBoundaryTests(unittest.TestCase):
    """D-12/GAP-46-01: the EVAL-02 canonical-frame pre-access boundary.

    ``pinn.evaluate.evaluate_run`` reconstructs and accesses the held-out
    ``test`` split (``StageIndex.from_split(adapter, manifest, "test")``)
    with NO canonical-frame assertion preceding it. D-12(b) requires "a
    pre-access assertion in the EVAL-02 invocation path that fails closed
    BEFORE any test-split materialization if the pairing is wrong" -- not
    merely before metric computation (57-RESEARCH.md "Common Pitfalls":
    "the frame assertion must run before any test StageIndex/adapter
    construction").
    """

    def test_tau_formula_matches_canonical_u_over_t(self) -> None:
        """D-12(a) dataset-free assembly regression: pins the ALREADY
        correct ``tau = 2*(t/T) - 1`` (i.e. ``u = t/T``) input construction
        so a future edit cannot silently drift it -- synthetic inputs only,
        no held-out access.
        """
        from pinn.constants import T_CHARACTERISTIC_TIME

        times = torch.tensor([0.0, 2.5, 5.0, 10.0], dtype=torch.float64)
        ic13 = torch.zeros(13, dtype=torch.float64)
        tau_ic13 = evaluate._build_tau_ic13(
            times, ic13, dtype=torch.float64, device=torch.device("cpu"),
        )
        expected_tau = 2.0 * (times / T_CHARACTERISTIC_TIME) - 1.0
        self.assertTrue(torch.allclose(tau_ic13[:, 0], expected_tau))

    def test_single_evaluator_claim_is_enforced(self) -> None:
        """D-15: exactly one invocation -- a second claim on the same
        owning run must refuse, never silently replay.
        """
        from datetime import datetime, timezone

        with tempfile.TemporaryDirectory() as tmp_dir:
            attempt_path = Path(tmp_dir) / "evaluation-attempt.json"
            run_dir = Path(tmp_dir)
            checkpoint_path = run_dir / "checkpoints" / "best.pt"
            evaluate._claim_evaluation_attempt(
                attempt_path, run_dir=run_dir, checkpoint_path=checkpoint_path,
                stamp=datetime.now(timezone.utc),
            )
            with self.assertRaises(evaluate.EvaluationReceiptExistsError):
                evaluate._claim_evaluation_attempt(
                    attempt_path, run_dir=run_dir,
                    checkpoint_path=checkpoint_path,
                    stamp=datetime.now(timezone.utc),
                )

    def test_frame_assertion_precedes_test_materialization(self) -> None:
        self.assertTrue(
            hasattr(evaluate, "assert_canonical_frame_precondition"),
            "pinn.evaluate must expose "
            "assert_canonical_frame_precondition() implementing the "
            "GAP-46-01 / D-12(b) pre-access assertion -- the canonical "
            "(r', u=t/T) pairing must be proved before any held-out "
            "test-split object is constructed or accessed",
        )
        source = inspect.getsource(evaluate.evaluate_run)
        assertion_pos = source.find("assert_canonical_frame_precondition(")
        materialize_pos = source.find("StageIndex.from_split(")
        self.assertNotEqual(
            assertion_pos, -1,
            "evaluate_run must call assert_canonical_frame_precondition()",
        )
        self.assertNotEqual(
            materialize_pos, -1,
            "evaluate_run must still construct the test split via "
            "StageIndex.from_split (the seam this ordering check protects)",
        )
        self.assertLess(
            assertion_pos, materialize_pos,
            "the canonical-frame assertion must execute BEFORE "
            "StageIndex.from_split constructs the held-out test split "
            "object (D-12(b): 'fails closed before any test-split "
            "materialization')",
        )


class EvidenceSelectionTests(unittest.TestCase):
    """Ports the Phase-50 four-structural-facts eligibility/selection pattern.

    v2.2 Phase 50's archived
    ``.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/evidence/
    build_phase50_evidence.py::{_structural_facts, cmd_candidate}`` computes
    four booleans per candidate run (``eval01_precondition_i``,
    ``guard_invariant_rule``, ``finished``, ``eval01_precondition_iii``;
    ``eligible = all(...)``) and selects the first eligible seed in FIXED
    order (42, 41, 43), never by any observed scientific metric, and never
    on a candidate whose artifact already contains an ``evaluation/``
    directory. Phase 57 ports this pattern into an importable production
    module (D-20: format is Claude's discretion) rather than the v2.2
    git-ledger-driven standalone CLI script, since RUN-05/EVAL-02 name
    ``pinn.verification`` as a target seam.

    ``importlib.util.find_spec`` (never a bare top-level ``import`` of the
    not-yet-existing module) so a genuinely missing module returns ``None``
    without raising any exception -- collection of THIS file, and every
    sibling class in it, must never fail because this module is absent.
    """

    MODULE_NAME = "pinn.verification.candidate_eligibility"

    def _module_or_fail(self):
        spec = importlib.util.find_spec(self.MODULE_NAME)
        self.assertIsNotNone(
            spec,
            f"{self.MODULE_NAME} must exist, porting the Phase-50 "
            "_structural_facts four-fact eligibility test "
            "(eval01_precondition_i, guard_invariant_rule, finished, "
            "eval01_precondition_iii) and a fixed-order (42, 41, 43) "
            "select_candidate(...) function -- metrics never affect "
            "selection and no candidate means no evaluation",
        )
        return importlib.import_module(self.MODULE_NAME)

    @staticmethod
    def _record(**overrides):
        base = {
            "eval01_precondition_i": True,
            "guard_invariant_rule": True,
            "finished": True,
            "eval01_precondition_iii": True,
        }
        base.update(overrides)
        return base

    def test_module_exists_with_structural_facts_and_selection(self) -> None:
        module = self._module_or_fail()
        self.assertTrue(hasattr(module, "structural_facts"))
        self.assertTrue(hasattr(module, "select_candidate"))

    def test_all_four_facts_true_is_eligible(self) -> None:
        module = self._module_or_fail()
        facts = module.structural_facts(self._record())
        self.assertTrue(facts["eligible"])

    def test_any_false_fact_is_ineligible(self) -> None:
        module = self._module_or_fail()
        for key in (
            "eval01_precondition_i", "guard_invariant_rule",
            "finished", "eval01_precondition_iii",
        ):
            facts = module.structural_facts(self._record(**{key: False}))
            self.assertFalse(
                facts["eligible"], f"{key}=False must make the record ineligible",
            )

    def test_selection_order_is_42_then_41_then_43(self) -> None:
        module = self._module_or_fail()
        facts_by_seed = {
            42: module.structural_facts(self._record()),
            41: module.structural_facts(self._record()),
            43: module.structural_facts(self._record()),
        }
        self.assertEqual(module.select_candidate(facts_by_seed), 42)

    def test_ineligible_42_falls_back_to_41_then_43(self) -> None:
        module = self._module_or_fail()
        facts_by_seed = {
            42: module.structural_facts(self._record(finished=False)),
            41: module.structural_facts(self._record()),
            43: module.structural_facts(self._record()),
        }
        self.assertEqual(module.select_candidate(facts_by_seed), 41)

    def test_no_eligible_seed_returns_none_not_an_invented_seed(self) -> None:
        module = self._module_or_fail()
        facts_by_seed = {
            seed: module.structural_facts(self._record(finished=False))
            for seed in (42, 41, 43)
        }
        self.assertIsNone(module.select_candidate(facts_by_seed))

    def test_selection_never_consults_a_metric_field(self) -> None:
        module = self._module_or_fail()
        # A record with a "better" observed metric must not out-rank the
        # fixed 42 -> 41 -> 43 order -- selection is structural-only.
        facts_by_seed = {
            42: module.structural_facts(self._record()),
            41: {**module.structural_facts(self._record()), "scs": -100.0},
            43: module.structural_facts(self._record()),
        }
        self.assertEqual(module.select_candidate(facts_by_seed), 42)


class RunFailureClassificationTests(unittest.TestCase):
    """Every run failure preserves the evaluation unspent, but only a
    completed GATE-04 refusal or an invariant-B no-advance HALT is the
    DECLARED terminal branch (57-CONTEXT.md "Declared terminal state");
    resource exhaustion, guard trips, and operational failures remain
    blocking/incomplete -- routed back for a fix/retry, not closed as a
    clean terminal outcome.
    """

    MODULE_NAME = "pinn.verification.candidate_eligibility"

    def _module_or_fail(self):
        spec = importlib.util.find_spec(self.MODULE_NAME)
        self.assertIsNotNone(
            spec,
            f"{self.MODULE_NAME} must exist and expose "
            "classify_run_outcome(outcome: str) -> {'terminal', 'blocking'}",
        )
        return importlib.import_module(self.MODULE_NAME)

    def test_gate04_refusal_is_the_declared_terminal_branch(self) -> None:
        module = self._module_or_fail()
        self.assertEqual(
            module.classify_run_outcome("gate04_block"), "terminal",
        )

    def test_invariant_b_no_advance_halt_is_the_declared_terminal_branch(self) -> None:
        module = self._module_or_fail()
        self.assertEqual(
            module.classify_run_outcome("invariant_b_halt_no_advance"),
            "terminal",
        )

    def test_resource_exhaustion_remains_blocking_incomplete(self) -> None:
        module = self._module_or_fail()
        self.assertEqual(
            module.classify_run_outcome("resource_exhaustion"), "blocking",
        )

    def test_guard_trip_remains_blocking_incomplete(self) -> None:
        module = self._module_or_fail()
        self.assertEqual(
            module.classify_run_outcome("guard_recover_exhausted"), "blocking",
        )

    def test_operational_failure_remains_blocking_incomplete(self) -> None:
        module = self._module_or_fail()
        self.assertEqual(
            module.classify_run_outcome("config_error"), "blocking",
        )

    def test_every_named_outcome_classifies_as_terminal_or_blocking_only(self) -> None:
        module = self._module_or_fail()
        for outcome in (
            "gate04_block", "invariant_b_halt_no_advance",
            "resource_exhaustion", "guard_recover_exhausted", "config_error",
        ):
            self.assertIn(
                module.classify_run_outcome(outcome), ("terminal", "blocking"),
                f"{outcome!r} must classify as exactly one of "
                "'terminal'/'blocking' -- no run failure classification "
                "authorizes spending EVAL-02 by itself; only a "
                "structurally-eligible, fully-preflighted, front-advancing "
                "run (EvidenceSelectionTests) ever reaches the evaluator",
            )
