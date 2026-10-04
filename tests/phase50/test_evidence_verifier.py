"""Independent identity, attempt, and terminal verifier fixtures for Plan 50-07."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.phase50._evidence_fixtures import (
    ARCHIVED_PHASE,
    AUTH_SUMMARY_REL,
    CONFIG_DELTA_REL,
    EVIDENCE,
    IDENTITY_BASELINE_REL,
    LEDGER_REL,
    PHASE,
    PRE_REG_REL,
    REPO_ROOT,
    SMOKE_AUTH_REL,
    SOURCE_MANIFEST_REL,
    VERIFIER,
    build_fixture,
    build_historical_repo,
    clone_complete,
    fail_closed_message,
    git,
    git_commit,
    git_head,
    script_env,
    sha256_text,
    write_text,
)


def run_real_terminal(repo: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(VERIFIER),
            "terminal",
            "--repo-root",
            str(repo),
            "--manifest",
            ".planning/phases/50-valid-stage-0-re-run/evidence/terminal-manifest.json",
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
        env=script_env(),
    )


class TerminalCompatibilityTests(unittest.TestCase):
    def test_historical_terminal_verifier_still_prints_ok(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = build_historical_repo(Path(tmp), with_runs=True)
            proc = run_real_terminal(repo)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("TERMINAL-EVIDENCE-OK", proc.stdout)
            for rel in (
                SOURCE_MANIFEST_REL,
                EVIDENCE / "band-record.md",
                EVIDENCE / "candidate-receipt.json",
                EVIDENCE / "manifest.json",
            ):
                self.assertFalse((repo / rel).exists())
                self.assertFalse(
                    (REPO_ROOT / ARCHIVED_PHASE / rel.relative_to(PHASE)).exists()
                )


class IdentityBaselineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.fx = build_fixture(Path(self.tmp.name) / "prereg", mode="preregistered")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_baseline_captures_generation_spans_and_referenced_hashes(self) -> None:
        output = self.fx.path(IDENTITY_BASELINE_REL)
        proc = self.fx.verify(
            "identity-baseline",
            ["--ledger", str(LEDGER_REL), "--output", str(IDENTITY_BASELINE_REL)],
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("IDENTITY-BASELINE-OK", proc.stdout)
        payload = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], "phase50-identity-baseline/v1")
        for generation in ("1", "2", "3"):
            self.assertRegex(payload["generation_object_sha256"][generation], r"^[0-9a-f]{64}$")
        self.assertIn("source_commit", payload)
        self.assertIn("source_tree", payload)
        self.assertTrue(payload["referenced_artifact_sha256"])


class IdentityAuthorizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.fx = build_fixture(Path(self.tmp.name) / "auth", mode="authorization")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_authorization_reads_committed_blob_and_trailer(self) -> None:
        proc = self.fx.verify(
            "identity",
            ["--state", "authorization", "--authorization-summary", str(AUTH_SUMMARY_REL)],
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("IDENTITY-OK", proc.stdout)

    def test_wrong_option_fails(self) -> None:
        text = self.fx.path(AUTH_SUMMARY_REL).read_text(encoding="utf-8")
        write_text(self.fx.path(AUTH_SUMMARY_REL), text.replace("authorize-preregistration", "stop-incomplete"))
        git_commit(self.fx.root, "docs: mutate authorization option")
        proc = self.fx.verify(
            "identity",
            ["--state", "authorization", "--authorization-summary", str(AUTH_SUMMARY_REL)],
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("FAIL-CLOSED", fail_closed_message(proc))

    def test_trailer_mismatch_fails(self) -> None:
        path = self.fx.path(AUTH_SUMMARY_REL)
        path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        git(self.fx.root, "add", str(AUTH_SUMMARY_REL))
        git(
            self.fx.root,
            "commit",
            "-m",
            "plan(50): bad trailer\n\nDecision-Summary-SHA256: " + ("0" * 64),
        )
        proc = self.fx.verify(
            "identity",
            ["--state", "authorization", "--authorization-summary", str(AUTH_SUMMARY_REL)],
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("FAIL-CLOSED", fail_closed_message(proc))

    def test_scope_mismatch_fails(self) -> None:
        text = self.fx.path(AUTH_SUMMARY_REL).read_text(encoding="utf-8")
        write_text(
            self.fx.path(AUTH_SUMMARY_REL),
            text.replace('"does_not_reopen_gap_50_03": true', '"does_not_reopen_gap_50_03": false'),
        )
        git_commit(self.fx.root, "docs: mutate scope")
        proc = self.fx.verify(
            "identity",
            ["--state", "authorization", "--authorization-summary", str(AUTH_SUMMARY_REL)],
        )
        self.assertNotEqual(proc.returncode, 0)

    def test_missing_ancestry_fails(self) -> None:
        text = self.fx.path(AUTH_SUMMARY_REL).read_text(encoding="utf-8")
        write_text(
            self.fx.path(AUTH_SUMMARY_REL),
            text.replace(self.fx.commits["50-06"], "deadbeef" * 5),
        )
        git_commit(self.fx.root, "docs: mutate ancestry")
        proc = self.fx.verify(
            "identity",
            ["--state", "authorization", "--authorization-summary", str(AUTH_SUMMARY_REL)],
        )
        self.assertNotEqual(proc.returncode, 0)

    def test_working_tree_authorization_is_ignored(self) -> None:
        path = self.fx.path(AUTH_SUMMARY_REL)
        path.write_text(path.read_text(encoding="utf-8") + "\n# dirty\n", encoding="utf-8")
        proc = self.fx.verify(
            "identity",
            ["--state", "authorization", "--authorization-summary", str(AUTH_SUMMARY_REL)],
        )
        self.assertNotEqual(proc.returncode, 0)


class IdentityPreregisteredTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.fx = build_fixture(Path(self.tmp.name) / "prereg", mode="preregistered")
        baseline = self.fx.verify(
            "identity-baseline",
            ["--ledger", str(LEDGER_REL), "--output", str(IDENTITY_BASELINE_REL)],
        )
        self.assertEqual(baseline.returncode, 0, baseline.stderr)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _identity(self, extra=None):
        args = [
            "--state",
            "preregistered",
            "--authorization-summary",
            str(AUTH_SUMMARY_REL),
            "--baseline",
            str(IDENTITY_BASELINE_REL),
            "--pre-registration",
            str(PRE_REG_REL),
            "--config-delta",
            str(CONFIG_DELTA_REL),
            "--ledger",
            str(LEDGER_REL),
        ]
        if extra:
            args.extend(extra)
        return self.fx.verify("identity", args)

    def test_preregistered_exact_match(self) -> None:
        proc = self._identity()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("IDENTITY-OK", proc.stdout)

    def test_recipe_mismatch_fails(self) -> None:
        path = self.fx.path("configs/stage0-rerun-seed42.yaml")
        path.write_text(path.read_text(encoding="utf-8").replace("n_adam: 1000", "n_adam: 999"), encoding="utf-8")
        git_commit(self.fx.root, "docs: mutate recipe")
        proc = self._identity()
        self.assertNotEqual(proc.returncode, 0)

    def test_source_tree_mismatch_fails(self) -> None:
        write_text(self.fx.path("pinn/changed.py"), "print('drift')\n")
        git_commit(self.fx.root, "docs: mutate source tree")
        proc = self._identity()
        self.assertNotEqual(proc.returncode, 0)

    def test_policy_mismatch_fails(self) -> None:
        text = self.fx.path(PRE_REG_REL).read_text(encoding="utf-8")
        write_text(self.fx.path(PRE_REG_REL), text.replace('"primary_seed": 42', '"primary_seed": 41'))
        git_commit(self.fx.root, "docs: mutate policy")
        proc = self._identity()
        self.assertNotEqual(proc.returncode, 0)

    def test_duplicate_generation_fails(self) -> None:
        text = self.fx.path(LEDGER_REL).read_text(encoding="utf-8")
        write_text(self.fx.path(LEDGER_REL), text.replace('"band_generation": 3', '"band_generation": 2', 1))
        proc = self._identity()
        self.assertNotEqual(proc.returncode, 0)

    def test_unopened_generation_invocation_fails(self) -> None:
        text = self.fx.path(LEDGER_REL).read_text(encoding="utf-8")
        write_text(
            self.fx.path(LEDGER_REL),
            text.replace('"records": []', '"records": [{"band_generation": 4, "run_name": "x", "attempt_ordinal": 1, "invocations": [{}]}]'),
        )
        proc = self._identity()
        self.assertNotEqual(proc.returncode, 0)

    def test_tracked_drift_fails(self) -> None:
        write_text(self.fx.path("pinn/__init__.py"), "# dirty tracked\n")
        proc = self._identity()
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("FAIL-CLOSED", fail_closed_message(proc))

    def test_untracked_drift_fails(self) -> None:
        write_text(self.fx.path("tests/phase50/sneak.py"), "print('untracked')\n")
        proc = self._identity()
        self.assertNotEqual(proc.returncode, 0)


class IdentityRunWindowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.fx = build_fixture(Path(self.tmp.name) / "runwin", mode="run-window")
        baseline = self.fx.verify(
            "identity-baseline",
            ["--ledger", str(LEDGER_REL), "--output", str(IDENTITY_BASELINE_REL)],
        )
        self.assertEqual(baseline.returncode, 0, baseline.stderr)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_run_window_accepts_smoke_authorization_at_decision_head(self) -> None:
        proc = self.fx.verify(
            "identity",
            [
                "--state",
                "run-window",
                "--authorization-summary",
                str(AUTH_SUMMARY_REL),
                "--smoke-authorization-summary",
                str(SMOKE_AUTH_REL),
                "--baseline",
                str(IDENTITY_BASELINE_REL),
                "--pre-registration",
                str(PRE_REG_REL),
                "--config-delta",
                str(CONFIG_DELTA_REL),
                "--ledger",
                str(LEDGER_REL),
            ],
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("IDENTITY-OK", proc.stdout)

    def test_run_window_rejects_head_after_smoke_authorization(self) -> None:
        git(self.fx.root, "commit", "--allow-empty", "-m", "docs: extra commit after smoke auth")
        proc = self.fx.verify(
            "identity",
            [
                "--state",
                "run-window",
                "--authorization-summary",
                str(AUTH_SUMMARY_REL),
                "--smoke-authorization-summary",
                str(SMOKE_AUTH_REL),
                "--baseline",
                str(IDENTITY_BASELINE_REL),
                "--pre-registration",
                str(PRE_REG_REL),
                "--config-delta",
                str(CONFIG_DELTA_REL),
                "--ledger",
                str(LEDGER_REL),
            ],
        )
        self.assertNotEqual(proc.returncode, 0)


class AttemptVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.fx = clone_complete(Path(self.tmp.name) / "attempt")
        extracted = self.fx.extract()
        self.assertEqual(extracted.returncode, 0, extracted.stderr)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _attempt(self, kind: str, seed: int | None, run_name: str):
        extra = [
            "--generation",
            "4",
            "--kind",
            kind,
            "--attempt-root",
            f"runs/{run_name}",
            "--ledger",
            str(LEDGER_REL),
            "--pre-registration",
            str(PRE_REG_REL),
        ]
        if seed is not None:
            extra.extend(["--seed", str(seed)])
        return self.fx.verify("attempt", extra)

    def test_smoke_and_graded_predecessor_chain(self) -> None:
        smoke = self._attempt("smoke", 42, "stage0-rerun-smoke")
        self.assertEqual(smoke.returncode, 0, smoke.stderr)
        self.assertIn("ATTEMPT-OK", smoke.stdout)
        for seed in (41, 42, 43):
            proc = self._attempt("graded", seed, f"stage0-rerun-seed{seed}")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("ATTEMPT-OK", proc.stdout)

    def test_failed_predecessor_makes_next_ineligible(self) -> None:
        summary = json.loads(
            (self.fx.attempt_roots["stage0-rerun-seed41"] / "summary.json").read_text(encoding="utf-8")
        )
        summary["disposition"] = "halted"
        write_text(
            self.fx.attempt_roots["stage0-rerun-seed41"] / "summary.json",
            json.dumps(summary, indent=2) + "\n",
        )
        proc = self._attempt("graded", 42, "stage0-rerun-seed42")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("FAIL-CLOSED", fail_closed_message(proc))

    def test_front_not_advanced_fails(self) -> None:
        log = self.fx.attempt_roots["stage0-rerun-seed43"] / "logs/train.log.jsonl"
        rewritten = []
        for line in log.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            row["front_idx"] = 0
            rewritten.append(json.dumps(row))
        write_text(log, "\n".join(rewritten) + "\n")
        proc = self._attempt("graded", 43, "stage0-rerun-seed43")
        self.assertNotEqual(proc.returncode, 0)

    def test_held_out_attempt_fails(self) -> None:
        eval_dir = self.fx.attempt_roots["stage0-rerun-seed42"] / "evaluation"
        eval_dir.mkdir()
        (eval_dir / "metrics.json").write_text("{}\n", encoding="utf-8")
        proc = self._attempt("graded", 42, "stage0-rerun-seed42")
        self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
