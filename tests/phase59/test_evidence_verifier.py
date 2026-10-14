"""Phase 59 evidence verifier on temporary git repositories."""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from pinn.verification.feasibility_scorecard import SCORECARD_SHA256


ROOT = Path(__file__).resolve().parents[2]
VERIFIER_PATH = (
    ROOT
    / ".planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py"
)
PHASE = ".planning/phases/59-read-only-baseline-scorecard"
DECISION_MODES = {
    f"{PHASE}/59-CONTEXT.md": "unchanged",
    f"{PHASE}/59-GAPS.md": "ancestor_state",
    f"{PHASE}/59-RESEARCH.md": "unchanged",
    f"{PHASE}/59-VALIDATION.md": "ancestor_state",
}


def load_verifier():
    if not VERIFIER_PATH.is_file():
        return None
    spec = importlib.util.spec_from_file_location(
        "phase59_evidence_verifier_under_test", VERIFIER_PATH
    )
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=False
    )
    if check and proc.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc


def init_repo(root: Path) -> None:
    _git(root, "init")
    _git(root, "config", "user.email", "phase59@example.com")
    _git(root, "config", "user.name", "phase59")


def commit_all(root: Path, message: str) -> str:
    _git(root, "add", "-A")
    _git(root, "commit", "-m", message)
    return _git(root, "rev-parse", "HEAD").stdout.strip()


def run_main(module, argv: list[str]) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = module.main(argv)
    return code, stdout.getvalue(), stderr.getvalue()


class FrozenRepo:
    """Copies of the real scorecard bytes plus decision-source stand-ins."""

    def __init__(self, root: Path) -> None:
        self.root = root
        init_repo(root)
        self._copy_frozen_inputs()
        self.sources = commit_all(root, "sources")
        self._write_freeze(self.sources)
        self.freeze = commit_all(root, "freeze")

    def _copy_frozen_inputs(self) -> None:
        copies = {
            "pinn/verification/artifacts/feasibility_scorecard_v1.json": ROOT
            / "pinn/verification/artifacts/feasibility_scorecard_v1.json",
            "pinn/verification/feasibility_scorecard.py": ROOT
            / "pinn/verification/feasibility_scorecard.py",
        }
        for relative, source in copies.items():
            dest = self.root / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(source.read_bytes())
        plain = self.root / f"{PHASE}/59-SCORECARD.md"
        plain.parent.mkdir(parents=True, exist_ok=True)
        plain.write_text("plain scorecard\n", encoding="utf-8")
        for relative in DECISION_MODES:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"{Path(relative).name} stand-in\n", encoding="utf-8")

    def pins(self, commit: str) -> dict:
        pins = {}
        for relative, mode in DECISION_MODES.items():
            blob = _git(self.root, "rev-parse", f"{commit}:{relative}").stdout.strip()
            raw = subprocess.check_output(
                ["git", "show", f"{commit}:{relative}"], cwd=self.root
            )
            last = _git(
                self.root, "log", "-1", "--format=%H", commit, "--", relative
            ).stdout.strip()
            pins[relative] = {
                "git_blob": blob,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "last_commit": last,
                "verify": mode,
            }
        return pins

    def _write_freeze(self, head: str, *, decision_sources: dict | None = None) -> None:
        evidence = self.root / f"{PHASE}/evidence"
        evidence.mkdir(parents=True, exist_ok=True)
        record = {
            "schema": "phase59-scorecard-freeze/v1",
            "scorecard_schema_version": "phase59-feasibility-scorecard/v1",
            "decisions_frozen": ["D-11"],
            "note": "test freeze",
            "phase_start_head": head,
            "head_at_freeze": head,
            "scorecard_path": "pinn/verification/artifacts/feasibility_scorecard_v1.json",
            "scorecard_module_path": "pinn/verification/feasibility_scorecard.py",
            "plain_doc_path": f"{PHASE}/59-SCORECARD.md",
        }
        for key in ("scorecard_path", "scorecard_module_path", "plain_doc_path"):
            raw = (self.root / record[key]).read_bytes()
            prefix = key.removesuffix("_path")
            record[f"{prefix}_sha256"] = hashlib.sha256(raw).hexdigest()
            record[f"{prefix}_size_bytes"] = len(raw)
        record["decision_sources"] = (
            self.pins(head) if decision_sources is None else decision_sources
        )
        if decision_sources is None:
            assert len(record) == 16
        (evidence / "scorecard-freeze.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    def rewrite_freeze(self, **updates) -> None:
        path = self.root / f"{PHASE}/evidence/scorecard-freeze.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        record.update(updates)
        path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class ScorecardFrozenTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_verifier()
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        if self.module is None:
            return
        self.repo = FrozenRepo(self.root)
        patcher = mock.patch.object(self.module, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_scorecard_frozen_passes_after_the_freeze_commit(self) -> None:
        self.assertIsNotNone(self.module)
        area = self.root / f"{PHASE}/evidence/census"
        area.mkdir(parents=True)
        (area / "census.json").write_text("{}\n", encoding="utf-8")
        commit_all(self.root, "census")
        code, out, err = run_main(self.module, ["scorecard-frozen"])
        self.assertEqual(err, "", err)
        self.assertEqual(code, 0)
        self.assertIn("SCORECARD-FROZEN-OK", out)

    def test_evidence_committed_before_or_with_the_freeze_fails(self) -> None:
        self.assertIsNotNone(self.module)
        early = self.root / f"{PHASE}/evidence/census"
        early.mkdir(parents=True)
        (early / "early.json").write_text("{}\n", encoding="utf-8")
        # Rebuild history: evidence exists before the freeze commit.
        sibling = tempfile.TemporaryDirectory()
        self.addCleanup(sibling.cleanup)
        other = Path(sibling.name)
        repo = FrozenRepo.__new__(FrozenRepo)
        repo.root = other
        init_repo(other)
        repo._copy_frozen_inputs()
        area = other / f"{PHASE}/evidence/census"
        area.mkdir(parents=True)
        (area / "census.json").write_text("{}\n", encoding="utf-8")
        commit_all(other, "evidence before freeze")
        head = _git(other, "rev-parse", "HEAD").stdout.strip()
        repo._write_freeze(head)
        commit_all(other, "freeze")
        with mock.patch.object(self.module, "REPO_ROOT", other):
            code, _out, err = run_main(self.module, ["scorecard-frozen"])
        self.assertEqual(code, 1)
        self.assertIn("ancestor", err)
        together = tempfile.TemporaryDirectory()
        self.addCleanup(together.cleanup)
        same = Path(together.name)
        same_repo = FrozenRepo.__new__(FrozenRepo)
        same_repo.root = same
        init_repo(same)
        same_repo._copy_frozen_inputs()
        head = commit_all(same, "sources")
        area = same / f"{PHASE}/evidence/census"
        area.mkdir(parents=True)
        (area / "census.json").write_text("{}\n", encoding="utf-8")
        same_repo._write_freeze(head)
        commit_all(same, "freeze and evidence")
        with mock.patch.object(self.module, "REPO_ROOT", same):
            code, _out, err = run_main(self.module, ["scorecard-frozen"])
        self.assertEqual(code, 1)
        self.assertIn("ancestor", err)

    def test_edited_or_dirty_scorecard_fails_and_pre_commit_checks_hashes(self) -> None:
        self.assertIsNotNone(self.module)
        scorecard = self.root / "pinn/verification/artifacts/feasibility_scorecard_v1.json"
        original = scorecard.read_bytes()
        scorecard.write_bytes(original + b" ")
        code, _out, err = run_main(self.module, ["scorecard-frozen"])
        self.assertEqual(code, 1)
        self.assertIn("dirty", err)
        scorecard.write_bytes(original)
        module_path = self.root / "pinn/verification/feasibility_scorecard.py"
        module_path.write_bytes(module_path.read_bytes() + b"\n# edited\n")
        commit_all(self.root, "edit rule module")
        code, _out, err = run_main(self.module, ["scorecard-frozen"])
        self.assertEqual(code, 1)
        self.assertNotIn("SCORECARD-FROZEN-OK", err)
        loose = tempfile.TemporaryDirectory()
        self.addCleanup(loose.cleanup)
        loose_root = Path(loose.name)
        loose_repo = FrozenRepo.__new__(FrozenRepo)
        loose_repo.root = loose_root
        init_repo(loose_root)
        loose_repo._copy_frozen_inputs()
        head = _git(loose_root, "write-tree").stdout.strip() if False else "0" * 40
        # Hashes match the on-disk files; nothing is committed.
        loose_repo.sources = "0" * 40
        # pins() needs a commit. Write the freeze record without decision git pins
        # only after committing sources so --pre-commit can ignore git.
        commit_all(loose_root, "sources")
        loose_repo._write_freeze(_git(loose_root, "rev-parse", "HEAD").stdout.strip())
        with mock.patch.object(self.module, "REPO_ROOT", loose_root):
            code, out, err = run_main(self.module, ["scorecard-frozen", "--pre-commit"])
        self.assertEqual(code, 0, err)
        self.assertIn("SCORECARD-FROZEN-OK", out)
        scorecard = loose_root / "pinn/verification/artifacts/feasibility_scorecard_v1.json"
        scorecard.write_bytes(scorecard.read_bytes() + b" ")
        with mock.patch.object(self.module, "REPO_ROOT", loose_root):
            code, _out, err = run_main(self.module, ["scorecard-frozen", "--pre-commit"])
        self.assertEqual(code, 1)
        self.assertIn(SCORECARD_SHA256[:12], err + scorecard.read_text(encoding="utf-8")[:0])

    def _repo_with_freeze(self, mutator) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        repo = FrozenRepo.__new__(FrozenRepo)
        repo.root = root
        init_repo(root)
        repo._copy_frozen_inputs()
        head = commit_all(root, "sources")
        repo.sources = head
        repo._write_freeze(head)
        path = root / f"{PHASE}/evidence/scorecard-freeze.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        mutator(repo, record)
        path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        commit_all(root, "freeze")
        return root

    def test_decision_source_pins_match_scorecard_frozen(self) -> None:
        self.assertIsNotNone(self.module)
        import pinn.verification.evidence_io as evidence_io

        def outcomes(root: Path) -> tuple[bool, bool]:
            with mock.patch.object(self.module, "REPO_ROOT", root):
                code, _out, _err = run_main(self.module, ["scorecard-frozen"])
            try:
                evidence_io.require_frozen_scorecard(repo_root=root)
            except evidence_io.FreezeNotEstablished:
                guard = False
            else:
                guard = True
            return code == 0, guard

        self.assertEqual(outcomes(self.root), (True, True))
        missing = self._repo_with_freeze(lambda _repo, record: record.pop("decision_sources"))
        self.assertEqual(outcomes(missing), (False, False))

    def test_wrong_blob_sha_or_last_commit_fails(self) -> None:
        self.assertIsNotNone(self.module)
        context = f"{PHASE}/59-CONTEXT.md"

        def bad_blob(_repo, record):
            record["decision_sources"][context]["git_blob"] = "a" * 40

        def bad_sha(_repo, record):
            record["decision_sources"][context]["sha256"] = "b" * 64

        def bad_last(repo, record):
            record["decision_sources"][context]["last_commit"] = repo.sources + "dead"

        for mutator, needle in (
            (bad_blob, "git_blob"),
            (bad_sha, "sha256"),
            (bad_last, "last_commit"),
        ):
            with self.subTest(needle=needle):
                root = self._repo_with_freeze(mutator)
                with mock.patch.object(self.module, "REPO_ROOT", root):
                    code, _out, err = run_main(self.module, ["scorecard-frozen"])
                self.assertEqual(code, 1)
                self.assertIn(needle, err)

    def test_unchanged_sources_reject_later_edits_and_ancestor_state_allows_them(self) -> None:
        self.assertIsNotNone(self.module)
        phase = self.root / PHASE
        (phase / "59-GAPS.md").write_text("gaps\nextra\n", encoding="utf-8")
        (phase / "59-VALIDATION.md").write_text("validation sign-off\n", encoding="utf-8")
        commit_all(self.root, "gaps and validation")
        code, out, err = run_main(self.module, ["scorecard-frozen"])
        self.assertEqual(code, 0, err)
        self.assertIn("SCORECARD-FROZEN-OK", out)
        (phase / "59-CONTEXT.md").write_text("context edited\n", encoding="utf-8")
        commit_all(self.root, "context")
        code, _out, err = run_main(self.module, ["scorecard-frozen"])
        self.assertEqual(code, 1)
        self.assertIn("59-CONTEXT.md", err)
        # Restore context and edit research instead.
        _git(self.root, "checkout", "HEAD~1", "--", f"{PHASE}/59-CONTEXT.md")
        commit_all(self.root, "restore context")
        (phase / "59-RESEARCH.md").write_text("research edited\n", encoding="utf-8")
        commit_all(self.root, "research")
        code, _out, err = run_main(self.module, ["scorecard-frozen"])
        self.assertEqual(code, 1)
        self.assertIn("59-RESEARCH.md", err)

    def test_real_worktree_prints_scorecard_frozen_ok(self) -> None:
        self.assertIsNotNone(self.module)
        code, out, err = run_main(self.module, ["scorecard-frozen"])
        self.assertEqual(code, 0, err)
        self.assertIn("SCORECARD-FROZEN-OK", out)
        self.assertNotIn("FAIL-CLOSED", err)


if __name__ == "__main__":
    unittest.main()
