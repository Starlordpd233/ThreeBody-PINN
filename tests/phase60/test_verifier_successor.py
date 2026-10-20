"""Phase 60 (D-09, GAP-60-02): the Phase 59 verifier and the one scorer successor.

Plan 60-02 fixed ``pinn/verification/feasibility_scorer.py``, which ten committed
Phase 59 result files pin by SHA-256. These tests run the Phase 59 verifier on
synthetic git repositories (the fixtures of ``tests.phase59.test_evidence_verifier``)
and prove that:

* a producer-digest mismatch is accepted for exactly one path, the scorer, and only
  when the committed ``scorer-successor.json`` names the digest the result recorded
  as the predecessor and the digest of the file on disk as the successor; every
  other mismatch is refused as before;
* a record that is absent, untracked, dirty, a symlink or malformed relaxes nothing;
* ``_rederive("baselines")`` hands ``baselines --check`` a temporary copy of the
  committed ``baselines/`` files in which only the predecessor digest is replaced
  by the successor digest (same length, every other byte identical), never writes
  the committed files, and fails the verifier instead of falling back to the
  unsubstituted run.

The stand-in scorer is a two-line file; the real digests appear only in the one
test that feeds the real record's bytes to the verifier's record rules.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from unittest import mock

from tests.phase59.test_evidence_verifier import (
    PHASE,
    AreaFixture,
    _dump,
    _git,
    _sha,
    commit_all,
)

ROOT = Path(__file__).resolve().parents[2]
SCORER = "pinn/verification/feasibility_scorer.py"
STUB = "pinn/verification/producer_stub.py"
RECORD_REL = (
    ".planning/phases/60-single-system-learnability/evidence/scorer-successor.json"
)
SCHEMA = "phase60-scorer-successor/v1"
OLD_SCORER = "scorer as Phase 59 produced it\n"
NEW_SCORER = "scorer with the MPS-safe widen\n"
BASELINES_REL = f"{PHASE}/evidence/baselines"
INTERPRETER_TAIL = ["-B", "-m", "pinn.verification.baselines", "--check"]


class SuccessorFixture(AreaFixture):
    """A synthetic repo whose census result pins a stand-in scorer by its old digest."""

    def setUp(self) -> None:
        super().setUp()
        self._ready()
        self.scorer = self.root / SCORER
        self.scorer.parent.mkdir(parents=True, exist_ok=True)
        self.scorer.write_text(OLD_SCORER, encoding="utf-8")
        self.old = _sha(self.scorer)
        self.new = hashlib.sha256(NEW_SCORER.encode("utf-8")).hexdigest()
        self.producer[SCORER] = self.old

    def record(self, **overrides) -> dict:
        payload = {
            "schema": SCHEMA,
            "path": SCORER,
            "predecessor_sha256": self.old,
            "successor_sha256": self.new,
            "reason": "stand-in for the GAP-59-13 scorer fix",
            "note": "synthetic successor record for the verifier tests",
        }
        payload.update(overrides)
        return payload

    def write_record(self, **overrides) -> Path:
        path = self.root / RECORD_REL
        _dump(path, self.record(**overrides))
        return path

    def commit_record(self, **overrides) -> Path:
        path = self.write_record(**overrides)
        commit_all(self.root, "scorer successor record")
        return path

    def advance_scorer(self) -> None:
        """Replace the stand-in scorer by its successor bytes, as Plan 60-02 did."""
        self.scorer.write_text(NEW_SCORER, encoding="utf-8")

    def check_census(self) -> tuple[int, str, str]:
        return self._run(["census", "--skip-rederive"])

    def pinned_census(self) -> None:
        """Census results that pin the old scorer digest, with the scorer already advanced."""
        self._write_census_tree()
        code, _out, err = self.check_census()
        self.assertEqual(code, 0, err)
        self.advance_scorer()

    def assert_refused(self, *fragments: str) -> None:
        code, out, err = self.check_census()
        self.assertEqual(code, 1, out)
        self.assertNotIn("CENSUS-OK", out)
        for fragment in fragments:
            self.assertIn(fragment, err)


class SuccessorAcceptedTests(SuccessorFixture):
    def test_the_committed_record_makes_the_area_check_pass(self) -> None:
        self.pinned_census()
        self.commit_record()
        code, out, err = self.check_census()
        self.assertEqual(code, 0, err)
        self.assertIn("CENSUS-OK", out)

    def test_the_record_is_read_at_call_time_from_the_module_repo_root(self) -> None:
        self.pinned_census()
        self.commit_record()
        self.assertEqual(self.module._scorer_successor()["path"], SCORER)
        (self.root / RECORD_REL).unlink()
        commit_all(self.root, "record removed")
        self.assertIsNone(self.module._scorer_successor())
        self.assert_refused("producer_sha256 does not match", SCORER)

    def test_the_real_phase_60_record_satisfies_the_verifier_rules(self) -> None:
        real = (ROOT / RECORD_REL).read_bytes()
        path = self.root / RECORD_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(real)
        commit_all(self.root, "the real record bytes")
        expected = json.loads(real)
        self.assertEqual(
            self.module._scorer_successor(),
            {key: expected[key] for key in ("path", "predecessor_sha256", "successor_sha256")},
        )


class SuccessorRefusedTests(SuccessorFixture):
    def test_a_record_naming_another_path_is_refused(self) -> None:
        self._write_census_tree()
        code, _out, err = self.check_census()
        self.assertEqual(code, 0, err)
        stub = self.root / STUB
        before = _sha(stub)
        stub.write_text("stub changed\n", encoding="utf-8")
        self.commit_record(path=STUB, predecessor_sha256=before, successor_sha256=_sha(stub))
        self.assert_refused("scorer successor record", f"not {SCORER}")

    def test_a_record_with_another_predecessor_is_refused(self) -> None:
        self.pinned_census()
        self.commit_record(predecessor_sha256="c" * 64)
        self.assert_refused("producer_sha256 does not match", SCORER)

    def test_a_record_with_another_successor_is_refused(self) -> None:
        self.pinned_census()
        self.commit_record(successor_sha256="d" * 64)
        self.assert_refused("producer_sha256 does not match", SCORER)

    def test_a_result_that_pins_neither_end_of_the_record_is_refused(self) -> None:
        self.pinned_census()
        path = self.root / f"{PHASE}/evidence/census/census.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["producer_sha256"][SCORER] = "e" * 64
        _dump(path, payload)
        code, _out, err = self._run(["manifest", "--area", "census", "--write"])
        self.assertEqual(code, 0, err)
        self.commit_record()
        self.assert_refused("producer_sha256 does not match", SCORER)

    def test_a_path_that_is_a_list_is_refused(self) -> None:
        self.pinned_census()
        self.commit_record(path=[SCORER])
        self.assert_refused("scorer successor record", "not a string")

    def test_a_predecessor_that_is_a_list_is_refused(self) -> None:
        self.pinned_census()
        self.commit_record(predecessor_sha256=[self.old])
        self.assert_refused("scorer successor record", "not a string")

    def test_a_successor_that_is_a_list_is_refused(self) -> None:
        self.pinned_census()
        self.commit_record(successor_sha256=[self.new])
        self.assert_refused("scorer successor record", "not a string")

    def test_a_record_with_a_list_of_successors_beside_the_pair_is_refused(self) -> None:
        self.pinned_census()
        self.commit_record(successors=[self.new, "f" * 64])
        self.assert_refused("scorer successor record", "exactly the keys")

    def test_a_record_with_a_list_of_paths_beside_the_path_is_refused(self) -> None:
        self.pinned_census()
        self.commit_record(paths=[SCORER, STUB])
        self.assert_refused("scorer successor record", "exactly the keys")

    def test_a_record_with_another_schema_is_refused(self) -> None:
        self.pinned_census()
        self.commit_record(schema="phase60-scorer-successor/v2")
        self.assert_refused("scorer successor record", "schema")

    def test_an_upper_case_digest_is_refused(self) -> None:
        self.pinned_census()
        self.commit_record(successor_sha256=self.new.upper())
        self.assert_refused("scorer successor record", "64 lowercase hex digits")

    def test_a_digest_with_a_trailing_newline_is_refused(self) -> None:
        self.pinned_census()
        self.commit_record(successor_sha256=self.new + "\n")
        self.assert_refused("scorer successor record", "64 lowercase hex digits")

    def test_a_record_that_is_not_json_is_refused(self) -> None:
        self.pinned_census()
        path = self.root / RECORD_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{not json", encoding="utf-8")
        commit_all(self.root, "garbled record")
        self.assert_refused("scorer successor record", "unreadable JSON")

    def test_a_record_that_is_a_json_list_is_refused(self) -> None:
        self.pinned_census()
        path = self.root / RECORD_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps([self.record()]), encoding="utf-8")
        commit_all(self.root, "list record")
        self.assert_refused("scorer successor record", "exactly the keys")

    def test_an_untracked_record_is_refused(self) -> None:
        self.pinned_census()
        self.write_record()
        self.assert_refused("scorer successor record is not tracked and clean")

    def test_a_record_with_an_uncommitted_modification_is_refused(self) -> None:
        self.pinned_census()
        self.commit_record()
        self.write_record(note="edited after the commit")
        self.assert_refused("scorer successor record is not tracked and clean")

    def test_a_staged_record_that_is_not_committed_is_refused(self) -> None:
        self.pinned_census()
        self.write_record()
        _git(self.root, "add", "--", RECORD_REL)
        self.assert_refused("scorer successor record is not tracked and clean")

    def test_a_record_that_is_a_symlink_is_refused(self) -> None:
        self.pinned_census()
        target = self.root / "elsewhere" / "record.json"
        _dump(target, self.record())
        link = self.root / RECORD_REL
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(target)
        commit_all(self.root, "symlinked record")
        self.assert_refused("scorer successor record", "symlink")


class OtherProducerTests(SuccessorFixture):
    def test_the_same_digest_pair_on_another_path_is_refused(self) -> None:
        # The stub starts and ends with exactly the scorer's old and new bytes, so
        # only the path tells the two producers apart.
        stub = self.root / STUB
        stub.write_text(OLD_SCORER, encoding="utf-8")
        self.producer[STUB] = self.old
        self._write_census_tree()
        code, _out, err = self.check_census()
        self.assertEqual(code, 0, err)
        self.advance_scorer()
        stub.write_text(NEW_SCORER, encoding="utf-8")
        self.assertEqual(_sha(stub), self.new)
        self.commit_record()
        self.assert_refused("producer_sha256 does not match", STUB)

    def test_a_mismatch_on_a_second_producer_is_refused_beside_a_valid_record(self) -> None:
        self.pinned_census()
        (self.root / STUB).write_text("stub changed\n", encoding="utf-8")
        self.commit_record()
        self.assertEqual(self.module._scorer_successor()["path"], SCORER)
        self.assert_refused("producer_sha256 does not match", STUB)

    def test_the_scorer_alone_changing_is_the_only_thing_the_record_excuses(self) -> None:
        self.pinned_census()
        self.commit_record()
        code, out, err = self.check_census()
        self.assertEqual(code, 0, err)
        self.assertIn("CENSUS-OK", out)
        (self.root / STUB).write_text("stub changed\n", encoding="utf-8")
        self.assert_refused("producer_sha256 does not match", STUB)


class AbsentRecordTests(SuccessorFixture):
    def test_a_scorer_change_without_a_record_fails_as_before(self) -> None:
        self.pinned_census()
        self.assertIsNone(self.module._scorer_successor())
        code, out, err = self.check_census()
        self.assertEqual(code, 1, out)
        self.assertIn(f"producer_sha256 does not match {SCORER}", err)
        self.assertNotIn("successor", err)

    def test_an_unchanged_scorer_passes_without_a_record(self) -> None:
        self._write_census_tree()
        code, out, err = self.check_census()
        self.assertEqual(code, 0, err)
        self.assertIn("CENSUS-OK", out)


class RederiveFixture(SuccessorFixture):
    """Committed baselines files, some of which embed the old scorer digest."""

    def setUp(self) -> None:
        super().setUp()
        old = self.old.encode("ascii")
        self.sources = {
            "baselines.json": b'{"producer_sha256": {"' + SCORER.encode() + b'": "' + old
            + b'"}, "again": "' + old + b'"}\n',
            "nn_copy.json": b'{"producer_sha256": {"x": "' + old + b'"}}\n',
            "summary.md": b"no digest in this file\n",
            "files_opened.json": b'{"test_split_opened": 0}\n',
            "two_kepler_population.csv": b"id,E\n1,0.5\n",
            "nested/inner.bin": b"\xff\xfe" + old + b"\x00tail",
            "logs/run.log": b"log " + old + b"\n",
            "__pycache__/mod.pyc": b"\x00" + old,
        }
        base = self.root / BASELINES_REL
        for name, raw in self.sources.items():
            path = base / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        self.advance_scorer()
        commit_all(self.root, "baselines tree")

    @contextlib.contextmanager
    def fake_interpreter(self, *, returncode: int = 0, stdout: str = "BASELINES-CHECK-OK\n"):
        """Replace subprocess.run for the interpreter only; git calls run for real."""
        calls: list[dict] = []
        real_run = subprocess.run

        def fake_run(argv, *args, **kwargs):
            if not argv or argv[0] != sys.executable:
                return real_run(argv, *args, **kwargs)
            call = {"argv": list(argv), "cwd": kwargs.get("cwd")}
            if "--evidence-root" in argv:
                root = Path(argv[argv.index("--evidence-root") + 1])
                call["root"] = root
                call["copy"] = {
                    path.relative_to(root / "baselines").as_posix(): path.read_bytes()
                    for path in sorted((root / "baselines").rglob("*"))
                    if path.is_file()
                }
            calls.append(call)
            return subprocess.CompletedProcess(argv, returncode, stdout=stdout, stderr="")

        with mock.patch.object(self.module.subprocess, "run", new=fake_run):
            yield calls

    def committed_names(self) -> set[str]:
        return {
            name for name in self.sources
            if not name.startswith(("logs/", "__pycache__/"))
        }


class SubstitutedRederiveTests(RederiveFixture):
    def test_baselines_are_checked_against_a_digest_substituted_copy(self) -> None:
        self.commit_record()
        with self.fake_interpreter() as calls:
            self.module._rederive("baselines")
        self.assertEqual(len(calls), 1)
        call = calls[0]
        self.assertIn("--evidence-root", call["argv"])
        root = call["root"]
        self.assertTrue(root.is_absolute())
        self.assertEqual(
            call["argv"],
            [sys.executable, *INTERPRETER_TAIL, "--evidence-root", str(root)],
        )
        self.assertEqual(call["cwd"], str(self.root))
        self.assertEqual(set(call["copy"]), self.committed_names())
        old, new = self.old.encode("ascii"), self.new.encode("ascii")
        for name, raw in call["copy"].items():
            source = self.sources[name]
            self.assertEqual(len(raw), len(source), name)
            self.assertEqual(raw, source.replace(old, new), name)
            self.assertNotIn(old, raw, name)
        embedding = {name for name in self.committed_names() if old in self.sources[name]}
        self.assertEqual(embedding, {"baselines.json", "nn_copy.json", "nested/inner.bin"})
        for name in embedding:
            self.assertIn(new, call["copy"][name], name)

    def test_the_committed_files_are_untouched_and_the_copy_is_removed(self) -> None:
        self.commit_record()
        with self.fake_interpreter() as calls:
            self.module._rederive("baselines")
        self.assertIn("--evidence-root", calls[0]["argv"])
        base = self.root / BASELINES_REL
        for name, raw in self.sources.items():
            self.assertEqual((base / name).read_bytes(), raw, name)
        status = _git(self.root, "status", "--porcelain", "--", BASELINES_REL)
        self.assertEqual(status.stdout.strip(), "")
        self.assertFalse(calls[0]["root"].exists())


class UnchangedRederiveTests(RederiveFixture):
    def test_without_a_record_the_original_command_runs(self) -> None:
        with self.fake_interpreter() as calls:
            self.module._rederive("baselines")
        self.assertEqual(
            [call["argv"] for call in calls], [[sys.executable, *INTERPRETER_TAIL]]
        )
        self.assertEqual(calls[0]["cwd"], str(self.root))

    def test_a_record_does_not_change_any_other_area(self) -> None:
        self.commit_record()
        for area in ("audit", "census", "survey"):
            tail, token = self.module.REDERIVE[area]
            with self.fake_interpreter(stdout=f"{token}\n") as calls:
                self.module._rederive(area)
            self.assertEqual([call["argv"] for call in calls], [[sys.executable, "-B", *tail]])


class SubstitutionFailureTests(RederiveFixture):
    def test_a_differing_substituted_check_fails_the_verifier(self) -> None:
        self.commit_record()
        with self.fake_interpreter(returncode=1, stdout="") as calls:
            with self.assertRaises(self.module.VerifyError) as caught:
                self.module._rederive("baselines")
        self.assertIn("baselines re-derivation exited 1", str(caught.exception))
        self.assertEqual(len(calls), 1)
        self.assertIn("--evidence-root", calls[0]["argv"])
        self.assertFalse(calls[0]["root"].exists())

    def test_a_check_that_does_not_print_its_token_fails_the_verifier(self) -> None:
        self.commit_record()
        with self.fake_interpreter(stdout="nothing useful\n"):
            with self.assertRaises(self.module.VerifyError) as caught:
                self.module._rederive("baselines")
        self.assertIn("baselines re-derivation did not print BASELINES-CHECK-OK", str(caught.exception))

    def test_an_untracked_record_stops_the_re_derivation_before_any_run(self) -> None:
        self.write_record()
        with self.fake_interpreter() as calls:
            with self.assertRaises(self.module.VerifyError) as caught:
                self.module._rederive("baselines")
        self.assertIn("scorer successor record is not tracked and clean", str(caught.exception))
        self.assertEqual(calls, [])

    def test_a_failed_copy_does_not_fall_back_to_the_unsubstituted_check(self) -> None:
        self.commit_record()
        with self.fake_interpreter() as calls:
            with mock.patch.object(self.module.shutil, "copytree", side_effect=OSError("disk full")):
                with self.assertRaises(OSError):
                    self.module._rederive("baselines")
        self.assertEqual(calls, [])
