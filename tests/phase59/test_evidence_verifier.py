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


def _plain(value):
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    return value


def _dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class AreaFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_verifier()
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        if self.module is None or "manifest" not in getattr(self.module, "COMMANDS", {}):
            return
        self.repo = FrozenRepo(self.root)
        self.patcher = mock.patch.object(self.module, "REPO_ROOT", self.root)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        stub = self.root / "pinn/verification/producer_stub.py"
        stub.parent.mkdir(parents=True, exist_ok=True)
        stub.write_text("stub\n", encoding="utf-8")
        self.producer = {"pinn/verification/producer_stub.py": _sha(stub)}
        self.card = __import__(
            "pinn.verification.feasibility_scorecard", fromlist=["load_scorecard"]
        ).load_scorecard()

    def _ready(self) -> None:
        self.assertIsNotNone(self.module)
        self.assertIn("manifest", self.module.COMMANDS)
        self.assertIn("census", self.module.COMMANDS)

    def _run(self, argv: list[str]) -> tuple[int, str, str]:
        return run_main(self.module, argv)

    def _producer_payload(self, schema: str, **extra) -> dict:
        payload = {
            "schema": schema,
            "plain_language": schema,
            "scorecard_sha256": SCORECARD_SHA256,
            "producer_sha256": dict(self.producer),
        }
        payload.update(extra)
        return payload

    def _write_retention(self, entries: list[dict]) -> None:
        _dump(
            self.root
            / ".planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/generation-7-retention.json",
            {"schema": "phase57-generation-retention/v1", "files": entries},
        )

    def _files_opened(self, **overrides) -> dict:
        payload = {
            "schema": "phase59-files-opened/v1",
            "tool": "phase59",
            "data_root_source": "test",
            "opened": {"train": 0, "validation": 0, "other_under_root": 0},
            "test_split_opened": 0,
            "blocked_attempts": 0,
            "refused_before_open": 0,
        }
        payload.update(overrides)
        return payload

    def _marker(self, area: str, step: str, names: list[str]) -> None:
        directory = self.root / f"{PHASE}/evidence" / area
        files = {name: _sha(directory / name) for name in names}
        _dump(
            directory / f"{step}.done.json",
            {
                "schema": "phase59-completion-marker/v1",
                "step": step,
                "command": "python -m phase59",
                "status": "complete",
                "utc_started": "2026-10-14T00:00:00+00:00",
                "utc_finished": "2026-10-14T00:00:01+00:00",
                "elapsed_seconds": 1.0,
                "ru_maxrss_bytes": 1,
                "preflight": {
                    "available_bytes": 10,
                    "required_bytes": 1,
                    "source": "vm_stat",
                },
                "result_files": files,
            },
        )

    def _write_census_tree(self) -> None:
        area = self.root / f"{PHASE}/evidence/census"
        ids = list(range(1, 1813))
        singles = [{"percentile": p, "target": p, "id": i, "N_in": 1.0, "samples_per_inner_period": 3.0} for p, i in zip((10, 50, 90), (1, 2, 3))]
        family = [{"bin": i, "size": 113, "median": 1.0, "id": 4 + i, "N_in": 2.0} for i in range(16)]
        validation = list(range(20001, 20228))
        csv_text = "id\n" + "\n".join(str(i) for i in ids) + "\n"
        (area).mkdir(parents=True, exist_ok=True)
        csv_path = area / "census.csv"
        csv_path.write_text(csv_text, encoding="utf-8")
        csv_hash = _sha(csv_path)
        rule = _plain(self.card.section("panel_rule"))
        _dump(
            area / "census.json",
            self._producer_payload(
                "phase59-census/v1",
                population={"train": 1812, "validation": 227},
                distributions={},
                checks={
                    "pair_tracking_failures": 0,
                    "gold_base_max_deviation": 0.0,
                    "gold_base_tolerance": 1e-6,
                    "unwrap_max_step_rad": 0.1,
                    "base_cross_check_flags": [],
                },
                phase_accuracy={},
                census_csv_sha256=csv_hash,
            ),
        )
        _dump(
            area / "panels.json",
            self._producer_payload(
                "phase59-panels/v1",
                rule=rule,
                census_csv_sha256=csv_hash,
                singles=singles,
                family=family,
                validation=validation,
            ),
        )
        _dump(area / "files_opened.json", self._files_opened(tool="census"))
        code, _out, err = self._run(["manifest", "--area", "census", "--write"])
        self.assertEqual(code, 0, err)

    def _write_audit_tree(self) -> None:
        splits = self.root / "runs/stage0-v23g7-seed42/splits.json"
        splits.parent.mkdir(parents=True, exist_ok=True)
        splits.write_text("{}\n", encoding="utf-8")
        self._write_retention(
            [{
                "path": "runs/stage0-v23g7-seed42/splits.json",
                "sha256": _sha(splits),
                "size_bytes": splits.stat().st_size,
                "role": "run-artifact",
            }]
        )
        area = self.root / f"{PHASE}/evidence/audit"
        _dump(
            area / "reader_acceptance.json",
            self._producer_payload(
                "phase59-reader-acceptance/v1",
                data_root_source="test",
                splits={
                    "sha256": _sha(splits),
                    "expected_from": "generation-7-retention",
                    "groups": {},
                    "allowed_physical_keys": [],
                    "withheld_physical_keys": [],
                },
                file_presence={},
                monitor_batch_reproduction={
                    "checkpoint": "stage-0-init.pt",
                    "rows": 1,
                    "identities": 1,
                    "mismatches_targets": 0,
                    "mismatches_times": 0,
                    "mismatches_masses": 0,
                    "ic13_max_abs": 0.0,
                    "ic13_tolerance": 1e-7,
                    "passed": True,
                },
                normalizer={
                    "source": "stage-0-init.pt",
                    "checkpoint": "stage-0-init.pt",
                    "slot_means": [],
                    "slot_stds": [],
                    "e_scale": 1.0,
                    "max_abs_residual": 0.0,
                    "tolerance": 1e-6,
                    "deviation": False,
                    "stats_sha256": "a" * 64,
                },
            ),
        )
        _dump(area / "files_opened.json", self._files_opened(tool="audit"))
        code, _out, err = self._run(["manifest", "--area", "audit", "--write"])
        self.assertEqual(code, 0, err)


class ManifestTests(AreaFixture):
    def test_manifest_round_trip_names_changed_missing_and_extra_files(self) -> None:
        self._ready()
        area = self.root / f"{PHASE}/evidence/census"
        area.mkdir(parents=True)
        (area / "census.json").write_text('{"a": 1}\n', encoding="utf-8")
        code, out, err = self._run(["manifest", "--area", "census", "--write"])
        self.assertEqual(code, 0, err)
        self.assertIn("MANIFEST-CENSUS-OK", out)
        manifest = json.loads((area / "MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["freeze_commit"], self.repo.freeze)
        self.assertEqual(manifest["produced_at_head"], _git(self.root, "rev-parse", "HEAD").stdout.strip())
        self.assertEqual(manifest["scorecard_sha256"], SCORECARD_SHA256)
        code, out, err = self._run(["manifest", "--area", "census"])
        self.assertEqual(code, 0, err)
        self.assertIn("MANIFEST-CENSUS-OK", out)
        target = area / "census.json"
        target.write_text('{"a": 2}\n', encoding="utf-8")
        code, _out, err = self._run(["manifest", "--area", "census"])
        self.assertEqual(code, 1)
        self.assertIn("census.json", err)
        target.write_text('{"a": 1}\n', encoding="utf-8")
        target.unlink()
        code, _out, err = self._run(["manifest", "--area", "census"])
        self.assertEqual(code, 1)
        self.assertIn("census.json", err)
        target.write_text('{"a": 1}\n', encoding="utf-8")
        (area / "extra.json").write_text("{}\n", encoding="utf-8")
        code, _out, err = self._run(["manifest", "--area", "census"])
        self.assertEqual(code, 1)
        self.assertIn("extra.json", err)


class AreaContractTests(AreaFixture):
    def test_census_contract_passes_and_named_breaks_fail(self) -> None:
        self._ready()
        self._write_census_tree()
        code, out, err = self._run(["census", "--skip-rederive"])
        self.assertEqual(code, 0, err)
        self.assertIn("CENSUS-OK", out)
        panels = self.root / f"{PHASE}/evidence/census/panels.json"
        payload = json.loads(panels.read_text(encoding="utf-8"))
        payload["rule"] = {"changed": True}
        _dump(panels, payload)
        self._run(["manifest", "--area", "census", "--write"])
        code, _out, err = self._run(["census", "--skip-rederive"])
        self.assertEqual(code, 1)
        self.assertIn("panel_rule", err)
        self._write_census_tree()
        payload = json.loads(panels.read_text(encoding="utf-8"))
        payload["census_csv_sha256"] = "b" * 64
        _dump(panels, payload)
        self._run(["manifest", "--area", "census", "--write"])
        code, _out, err = self._run(["census", "--skip-rederive"])
        self.assertEqual(code, 1)
        self.assertIn("census.csv", err)
        self._write_census_tree()
        payload = json.loads(panels.read_text(encoding="utf-8"))
        payload["family"][0]["id"] = payload["singles"][0]["id"]
        _dump(panels, payload)
        self._run(["manifest", "--area", "census", "--write"])
        code, _out, err = self._run(["census", "--skip-rederive"])
        self.assertEqual(code, 1)
        self.assertIn("family", err)
        opened = self.root / f"{PHASE}/evidence/census/files_opened.json"
        _dump(opened, self._files_opened(tool="census", test_split_opened=1))
        self._run(["manifest", "--area", "census", "--write"])
        code, _out, err = self._run(["census", "--skip-rederive"])
        self.assertEqual(code, 1)
        self.assertIn("test_split_opened", err)


class RederiveTests(AreaFixture):
    def test_census_rederive_uses_the_patched_table(self) -> None:
        self._ready()
        self.assertIn("census", self.module.REDERIVE)
        self._write_census_tree()
        with mock.patch.dict(
            self.module.REDERIVE,
            {"census": (["-c", "print('CENSUS-CHECK-OK')"], "CENSUS-CHECK-OK")},
        ):
            code, out, err = self._run(["census"])
        self.assertEqual(code, 0, err)
        self.assertIn("CENSUS-OK", out)
        with mock.patch.dict(
            self.module.REDERIVE,
            {"census": (["-c", "import sys; sys.exit(1)"], "CENSUS-CHECK-OK")},
        ):
            code, _out, err = self._run(["census"])
        self.assertEqual(code, 1)
        self.assertNotIn("CENSUS-CHECK-OK", err + _out if False else err)
        with mock.patch.dict(
            self.module.REDERIVE,
            {"census": (["-c", "print('NO')"], "CENSUS-CHECK-OK")},
        ):
            code, _out, err = self._run(["census"])
        self.assertEqual(code, 1)
        self.assertIn("CENSUS-CHECK-OK", err)


class AuditTests(AreaFixture):
    def test_audit_fails_on_monitor_or_normalizer(self) -> None:
        self._ready()
        self.assertIn("audit", self.module.COMMANDS)
        self._write_audit_tree()
        code, out, err = self._run(["audit", "--skip-rederive"])
        self.assertEqual(code, 0, err)
        self.assertIn("AUDIT-OK", out)
        path = self.root / f"{PHASE}/evidence/audit/reader_acceptance.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["monitor_batch_reproduction"]["passed"] = False
        _dump(path, payload)
        self._run(["manifest", "--area", "audit", "--write"])
        code, _out, err = self._run(["audit", "--skip-rederive"])
        self.assertEqual(code, 1)
        self.assertIn("passed", err)
        self._write_audit_tree()
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["normalizer"]["max_abs_residual"] = 1.0
        payload["normalizer"]["deviation"] = False
        _dump(path, payload)
        self._run(["manifest", "--area", "audit", "--write"])
        code, _out, err = self._run(["audit", "--skip-rederive"])
        self.assertEqual(code, 1)
        self.assertIn("normalizer", err)


class Diag07Tests(AreaFixture):
    def _checkpoint(self) -> dict:
        path = self.root / "runs/stage0-v23g7-seed42/checkpoints/best.pt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"checkpoint")
        entry = {
            "path": "runs/stage0-v23g7-seed42/checkpoints/best.pt",
            "sha256": _sha(path),
            "size_bytes": path.stat().st_size,
            "role": "run-artifact",
        }
        self._write_retention([entry])
        return {
            "run": "stage0-v23g7-seed42",
            "file": "best.pt",
            "path": entry["path"],
            "sha256": entry["sha256"],
            "size_bytes": entry["size_bytes"],
            "global_step": 900,
            "adam_step": 900,
        }

    def _jx(self, name: str, checkpoint: dict) -> None:
        _dump(
            self.root / f"{PHASE}/evidence/diag07" / name,
            self._producer_payload(
                "phase59-diag07-result/v1",
                experiment=name[:-5],
                command="python -m diag07",
                code_identity={
                    "commit": self.card.section("diag07")["code_commit"],
                    "snapshot_files": [],
                    "snapshot_digest": "c" * 64,
                    "pinn_module_root": "pinn",
                    "overlay_modules": [],
                },
                runtimes=[],
                checkpoints=[checkpoint],
                results={},
                reading={"question": "q", "supports": "", "falsifies": "", "outcome": "neither"},
                tolerance_checks=[{"name": "share", "passed": True, "detail": "ok"}],
                memory={"ru_maxrss_bytes": 1},
                non_interference={
                    "parameters_unchanged": True,
                    "grads_none": True,
                    "optimizer_constructed": True,
                    "checkpoint_writes": 0,
                    "runs_hashes_unchanged": True,
                },
                files_opened=self._files_opened(tool=name),
            ),
        )

    def test_diag07_recomputes_gate_g1_and_honors_require(self) -> None:
        self._ready()
        self.assertIn("diag07", self.module.COMMANDS)
        from pinn.verification.feasibility_scorecard import g1_fires

        checkpoint = self._checkpoint()
        self._jx("jx01.json", checkpoint)
        expected = g1_fires({900: 1e-3, 951: 2e-3}, scorecard=self.card)
        _dump(
            self.root / f"{PHASE}/evidence/diag07/g1.json",
            self._producer_payload(
                "phase59-gate-g1/v1",
                threshold=0.01,
                primary_share={"900": 1e-3, "951": 2e-3},
                secondary_share={"900": 0.0, "951": 0.0},
                fires=expected["fires"],
                outcome=expected["outcome"],
                source_sha256=_sha(self.root / f"{PHASE}/evidence/diag07/jx01.json"),
            ),
        )
        self._marker("diag07", "jx01", ["jx01.json", "g1.json"])
        _dump(self.root / f"{PHASE}/evidence/diag07/files_opened.json", self._files_opened(tool="diag07"))
        code, _out, err = self._run(["manifest", "--area", "diag07", "--write"])
        self.assertEqual(code, 0, err)
        code, out, err = self._run(["diag07", "--skip-rederive"])
        self.assertEqual(code, 0, err)
        self.assertIn("DIAG07-OK", out)
        g1 = json.loads((self.root / f"{PHASE}/evidence/diag07/g1.json").read_text(encoding="utf-8"))
        g1["fires"] = True
        _dump(self.root / f"{PHASE}/evidence/diag07/g1.json", g1)
        self._marker("diag07", "jx01", ["jx01.json", "g1.json"])
        self._run(["manifest", "--area", "diag07", "--write"])
        code, _out, err = self._run(["diag07", "--skip-rederive"])
        self.assertEqual(code, 1)
        self.assertIn("g1_fires", err)
        code, _out, err = self._run(["diag07", "--skip-rederive", "--require", "jx01,jx10"])
        self.assertEqual(code, 1)
        self.assertIn("jx10.json", err)


class FreezeInAreaTests(AreaFixture):
    def test_area_commands_fail_before_area_checks_when_the_freeze_fails(self) -> None:
        self._ready()
        self._write_census_tree()
        module = self.root / "pinn/verification/feasibility_scorecard.py"
        module.write_bytes(module.read_bytes() + b"\n# edited\n")
        code, _out, err = self._run(["census", "--skip-rederive"])
        self.assertEqual(code, 1)
        self.assertIn("sha256", err)
        self.assertNotIn("panel_rule", err)
        module.write_bytes(ROOT / "pinn/verification/feasibility_scorecard.py")
        code, out, err = self._run(["manifest", "--area", "census", "--write"])
        self.assertEqual(code, 0, err)
        manifest = json.loads((self.root / f"{PHASE}/evidence/census/MANIFEST.json").read_text(encoding="utf-8"))
        manifest["freeze_commit"] = "a" * 40
        _dump(self.root / f"{PHASE}/evidence/census/MANIFEST.json", manifest)
        code, _out, err = self._run(["manifest", "--area", "census"])
        self.assertEqual(code, 1)
        self.assertIn("freeze_commit", err)
        manifest["freeze_commit"] = self.repo.freeze
        manifest["produced_at_head"] = "b" * 40
        _dump(self.root / f"{PHASE}/evidence/census/MANIFEST.json", manifest)
        code, _out, err = self._run(["manifest", "--area", "census"])
        self.assertEqual(code, 1)
        self.assertIn("produced_at_head", err)


class RequireCommittedTests(AreaFixture):
    def test_require_committed_rejects_dirty_history_and_accepts_two_producers(self) -> None:
        self._ready()
        self._write_census_tree()
        code, _out, err = self._run(["census", "--skip-rederive", "--require-committed"])
        self.assertEqual(code, 1)
        self.assertTrue("tracked" in err or "clean" in err or "commit" in err)
        commit_all(self.root, "census")
        code, out, err = self._run(["census", "--skip-rederive", "--require-committed"])
        self.assertEqual(code, 0, err)
        self.assertIn("CENSUS-OK", out)
        target = self.root / f"{PHASE}/evidence/census/census.json"
        original = target.read_bytes()
        target.write_bytes(original + b" ")
        code, _out, err = self._run(["census", "--skip-rederive", "--require-committed"])
        self.assertEqual(code, 1)
        target.write_bytes(original)
        # A manifest whose produced_at_head is a side commit is not an ancestor of its own commit.
        side = _git(self.root, "checkout", "-b", "side")
        self.assertEqual(side.returncode, 0, side.stderr)
        commit_all(self.root, "side") if False else _git(self.root, "commit", "--allow-empty", "-m", "side")
        side_sha = _git(self.root, "rev-parse", "HEAD").stdout.strip()
        back = _git(self.root, "checkout", "-")
        self.assertEqual(back.returncode, 0, back.stderr)
        manifest_path = self.root / f"{PHASE}/evidence/census/MANIFEST.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["produced_at_head"] = side_sha
        _dump(manifest_path, manifest)
        commit_all(self.root, "manifest points at side")
        code, _out, err = self._run(["census", "--skip-rederive", "--require-committed"])
        self.assertEqual(code, 1)
        self.assertIn("produced_at_head", err)
        # Second producer adds a file and rewrites the manifest at the later head.
        manifest["produced_at_head"] = _git(self.root, "rev-parse", "HEAD").stdout.strip()
        _dump(manifest_path, manifest)
        extra = self.root / f"{PHASE}/evidence/census/note.json"
        _dump(extra, self._producer_payload("phase59-census-note/v1"))
        code, _out, err = self._run(["manifest", "--area", "census", "--write"])
        self.assertEqual(code, 0, err)
        commit_all(self.root, "second producer")
        code, out, err = self._run(["census", "--skip-rederive", "--require-committed"])
        self.assertEqual(code, 0, err)
        self.assertIn("CENSUS-OK", out)


class ProducerHashTests(AreaFixture):
    def test_result_producer_hash_must_match_current_bytes(self) -> None:
        self._ready()
        self._write_census_tree()
        path = self.root / f"{PHASE}/evidence/census/census.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload.pop("producer_sha256")
        _dump(path, payload)
        self._run(["manifest", "--area", "census", "--write"])
        code, _out, err = self._run(["census", "--skip-rederive"])
        self.assertEqual(code, 1)
        self.assertIn("producer_sha256", err)
        self._write_census_tree()
        stub = self.root / "pinn/verification/producer_stub.py"
        stub.write_text("changed\n", encoding="utf-8")
        code, _out, err = self._run(["census", "--skip-rederive"])
        self.assertEqual(code, 1)
        self.assertIn("pinn/verification/producer_stub.py", err)


class CompletionMarkerTests(AreaFixture):
    def test_survey_and_diag07_require_a_matching_marker(self) -> None:
        self._ready()
        self.assertIn("survey", self.module.COMMANDS)
        area = self.root / f"{PHASE}/evidence/survey"
        _dump(
            area / "survey.json",
            self._producer_payload("phase59-survey/v1"),
        )
        _dump(
            area / "picks.json",
            self._producer_payload(
                "phase59-feas09-picks/v1",
                stage4b={"no_pick": "empty"},
                stage6={"record": "a", "value": 1, "rule": "nearest", "sensitivity": "low"},
            ),
        )
        _dump(area / "files_opened.json", self._files_opened(tool="survey"))
        self._run(["manifest", "--area", "survey", "--write"])
        code, _out, err = self._run(["survey", "--skip-rederive"])
        self.assertEqual(code, 1)
        self.assertIn("marker", err)
        self._marker("survey", "survey", ["survey.json", "picks.json"])
        marker = json.loads((area / "survey.done.json").read_text(encoding="utf-8"))
        marker["status"] = "partial"
        _dump(area / "survey.done.json", marker)
        self._run(["manifest", "--area", "survey", "--write"])
        code, _out, err = self._run(["survey", "--skip-rederive"])
        self.assertEqual(code, 1)
        self.assertIn("complete", err)
        self._marker("survey", "survey", ["survey.json", "picks.json"])
        marker = json.loads((area / "survey.done.json").read_text(encoding="utf-8"))
        marker["result_files"]["survey.json"] = "d" * 64
        _dump(area / "survey.done.json", marker)
        self._run(["manifest", "--area", "survey", "--write"])
        code, _out, err = self._run(["survey", "--skip-rederive"])
        self.assertEqual(code, 1)
        self.assertIn("survey.json", err)
        self._marker("survey", "survey", ["survey.json", "picks.json"])
        self._run(["manifest", "--area", "survey", "--write"])
        code, out, err = self._run(["survey", "--skip-rederive"])
        self.assertEqual(code, 0, err)
        self.assertIn("SURVEY-OK", out)


from typing import Mapping  # noqa: E402  (helpers above use Mapping)


if __name__ == "__main__":
    unittest.main()
