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

import json
import math
import unittest
from pathlib import Path

import torch

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
