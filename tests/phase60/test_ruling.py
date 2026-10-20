"""Phase 60 (D-11, GAP-60-09, GAP-60-11): tests for the owner ruling loaders.

The loaders read the owner's answers from committed files and from nothing else. These
tests prove the file contract: one strict machine block, one opaque quote block, closed
key sets, plain-decimal values, a tracked and clean file, and a SHA-256 that every
continue-path record can cite.

Every ruling file in this module is a synthetic fixture in a temporary directory. The
quote text is a stand-in that says so; no real owner message, and no real ruling file of
the project, is read, written or copied here.
"""

from __future__ import annotations

import ast
import dataclasses
import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from pinn.verification import learnability_ruling as ruling
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.learnability_arms import PHASE_REL
from tests.phase59.test_evidence_verifier import commit_all, init_repo

ROOT = Path(__file__).resolve().parents[2]
CARD = load_scorecard()
QUOTE = "Synthetic fixture text standing in for a message. It is not an owner statement."
PROSE = (
    "Prose outside the blocks is ignored by the loader: answer: go-to-verdict and "
    "approved_first_omega_0: 5 mean nothing here.\n"
)


def ruling_file(machine_lines, *, quote=QUOTE, machine_fence="```", quote_fence="```",
                prose=PROSE, quote_first=False):
    """A synthetic ruling file: front matter, prose, one machine block and one quote block."""
    machine = f"{machine_fence}phase60-ruling\n" + "\n".join(machine_lines) + f"\n{machine_fence}\n"
    owner = f"{quote_fence}owner-quote\n{quote}\n{quote_fence}\n"
    front = "---\nphase: 60-single-system-learnability\nstatus: fixture\n---\n\n# Synthetic ruling\n\n"
    blocks = (owner + "\n" + machine) if quote_first else (machine + "\n" + owner)
    return front + prose + "\n" + blocks


def checkpoint4(answer="continue", value="120", **kwargs):
    lines = ["ruling: checkpoint-4", f"answer: {answer}"]
    if value is not None:
        lines.append(f"approved_first_omega_0: {value}")
    return ruling_file(lines, **kwargs)


def gap6009(reading="no_rescue", **kwargs):
    return ruling_file(["ruling: gap-60-09", f"reading: {reading}"], **kwargs)


def parse4(text):
    return ruling.parse_machine_block(text, kind="checkpoint-4")


def parse9(text):
    return ruling.parse_machine_block(text, kind="gap-60-09")


class MachineBlockTests(unittest.TestCase):
    def test_a_continue_ruling_parses_to_its_answer_and_value(self):
        self.assertEqual(parse4(checkpoint4("continue", "120")),
                         {"answer": "continue", "approved_first_omega_0": 120.0})

    def test_a_value_off_the_sweep_grid_parses(self):
        self.assertEqual(parse4(checkpoint4("continue", "37.5"))["approved_first_omega_0"], 37.5)
        self.assertEqual(parse4(checkpoint4("continue", "0.25"))["approved_first_omega_0"], 0.25)
        self.assertEqual(parse4(checkpoint4("continue", "030"))["approved_first_omega_0"], 30.0)

    def test_go_to_verdict_parses_without_a_value(self):
        self.assertEqual(parse4(checkpoint4("go-to-verdict", None)),
                         {"answer": "go-to-verdict", "approved_first_omega_0": None})

    def test_a_gap_60_09_reading_parses(self):
        for reading in ("no_rescue", "rescue"):
            with self.subTest(reading=reading):
                self.assertEqual(parse9(gap6009(reading)), {"reading": reading})

    def test_a_continue_without_a_value_is_refused(self):
        with self.assertRaises(ruling.RulingError):
            parse4(checkpoint4("continue", None))

    def test_a_value_that_is_not_a_plain_positive_decimal_is_refused(self):
        for bad in (
            "0", "0.0", "00", "-60", "-0.5", "nan", "NaN", "inf", "Infinity", "-inf",
            "1e3", "1E3", "1.5e1", "120 # note", "120 note", "+120", ".5", "120.", "1,000",
            "0x10", "1_000", "12 0", "twelve", "\u0661\u0662\u0660", "120\u00a0", "1" * 400, "0.0000",
        ):
            with self.subTest(value=bad):
                with self.assertRaises(ruling.RulingError):
                    parse4(checkpoint4("continue", bad))

    def test_a_value_beside_a_go_to_verdict_answer_is_refused(self):
        with self.assertRaises(ruling.RulingError):
            parse4(checkpoint4("go-to-verdict", "120"))

    def test_an_answer_outside_the_closed_set_is_refused(self):
        for bad in ("Continue", "CONTINUE", "yes", "go to the verdict", "go_to_verdict",
                    "continue,go-to-verdict", ""):
            for value_lines in (["approved_first_omega_0: 120"], []):
                with self.subTest(answer=bad, with_value=bool(value_lines)):
                    with self.assertRaises(ruling.RulingError):
                        parse4(ruling_file(["ruling: checkpoint-4", f"answer: {bad}",
                                            *value_lines]))

    def test_a_reading_outside_the_closed_set_is_refused(self):
        for bad in ("Rescue", "no rescue", "norescue", "maybe", "continue", ""):
            with self.subTest(reading=bad):
                with self.assertRaises(ruling.RulingError):
                    parse9(gap6009(bad))

    def test_a_duplicate_key_is_refused(self):
        for lines in (
            ["ruling: checkpoint-4", "answer: continue", "answer: continue",
             "approved_first_omega_0: 120"],
            ["ruling: checkpoint-4", "answer: continue", "approved_first_omega_0: 120",
             "approved_first_omega_0: 120"],
            ["ruling: checkpoint-4", "ruling: checkpoint-4", "answer: go-to-verdict"],
        ):
            with self.subTest(lines=lines):
                with self.assertRaises(ruling.RulingError):
                    parse4(ruling_file(lines))
        with self.assertRaises(ruling.RulingError):
            parse9(ruling_file(["ruling: gap-60-09", "reading: rescue", "reading: no_rescue"]))

    def test_an_unknown_key_is_refused(self):
        for extra in ("note: fine", "approved_first_omega_1: 5", "Answer: continue",
                      "first_omega_0: 120", "reading: rescue"):
            with self.subTest(extra=extra):
                with self.assertRaises(ruling.RulingError):
                    parse4(ruling_file(["ruling: checkpoint-4", "answer: continue",
                                        "approved_first_omega_0: 120", extra]))
        with self.assertRaises(ruling.RulingError):
            parse9(ruling_file(["ruling: gap-60-09", "reading: rescue", "answer: continue"]))

    def test_the_ruling_line_must_name_the_kind(self):
        for line in ("ruling: checkpoint-5", "ruling: gap-60-09", "ruling: Checkpoint-4", ""):
            with self.subTest(line=line):
                with self.assertRaises(ruling.RulingError):
                    parse4(ruling_file([line, "answer: go-to-verdict"]))
        with self.assertRaises(ruling.RulingError):
            parse4(ruling_file(["answer: go-to-verdict"]))  # no ruling line at all
        with self.assertRaises(ruling.RulingError):
            parse9(ruling_file(["ruling: checkpoint-4", "reading: rescue"]))
        with self.assertRaises(ruling.RulingError):
            parse4(gap6009("rescue"))

    def test_a_missing_answer_is_refused(self):
        with self.assertRaises(ruling.RulingError):
            parse4(ruling_file(["ruling: checkpoint-4", "approved_first_omega_0: 120"]))
        with self.assertRaises(ruling.RulingError):
            parse9(ruling_file(["ruling: gap-60-09"]))

    def test_a_line_that_is_not_key_colon_value_is_refused(self):
        for line in ("this is not a key line", "answer continue", "answer:continue",
                     "# a comment", "- answer: continue", "  answer: continue", ": continue"):
            with self.subTest(line=line):
                with self.assertRaises(ruling.RulingError):
                    parse4(ruling_file(["ruling: checkpoint-4", "answer: continue",
                                        "approved_first_omega_0: 120", line]))

    def test_an_indented_key_line_is_not_a_key_line(self):
        for lines in (
            ["ruling: checkpoint-4", "  answer: go-to-verdict"],
            ["  ruling: checkpoint-4", "answer: go-to-verdict"],
            ["ruling: checkpoint-4", "\tanswer: go-to-verdict"],
        ):
            with self.subTest(lines=lines):
                with self.assertRaises(ruling.RulingError):
                    parse4(ruling_file(lines))

    def test_blank_lines_inside_the_block_are_ignored(self):
        text = ruling_file(["", "ruling: checkpoint-4", "", "answer: continue",
                            "approved_first_omega_0: 120", ""])
        self.assertEqual(parse4(text)["approved_first_omega_0"], 120.0)

    def test_no_machine_block_or_two_machine_blocks_are_refused(self):
        with self.assertRaises(ruling.RulingError):
            parse4("# no blocks at all\n\n```owner-quote\n" + QUOTE + "\n```\n")
        two = checkpoint4("continue", "120") + "\n```phase60-ruling\nruling: checkpoint-4\nanswer: go-to-verdict\n```\n"
        with self.assertRaises(ruling.RulingError):
            parse4(two)

    def test_the_info_string_must_be_exact(self):
        for info in ("phase60-ruling extra", "PHASE60-RULING", "phase60-ruling,", "phase60", ""):
            with self.subTest(info=info):
                text = (f"```{info}\nruling: checkpoint-4\nanswer: go-to-verdict\n```\n\n"
                        f"```owner-quote\n{QUOTE}\n```\n")
                with self.assertRaises(ruling.RulingError):
                    parse4(text)

    def test_an_indented_fence_is_a_fence_up_to_three_spaces_and_not_beyond(self):
        body = "ruling: checkpoint-4\nanswer: go-to-verdict\n"
        quote = f"```owner-quote\n{QUOTE}\n```\n"
        self.assertEqual(parse4(f"   ```phase60-ruling\n{body}   ```\n\n{quote}")["answer"],
                         "go-to-verdict")
        with self.assertRaises(ruling.RulingError):
            parse4(f"    ```phase60-ruling\n{body}    ```\n\n{quote}")

    def test_tilde_fences_work_and_a_longer_fence_closes_a_shorter_one(self):
        body = "ruling: checkpoint-4\nanswer: go-to-verdict"
        text = f"~~~phase60-ruling\n{body}\n~~~~~~\n\n```owner-quote\n{QUOTE}\n```\n"
        self.assertEqual(parse4(text)["answer"], "go-to-verdict")
        # a fence of the other character, or a shorter one, does not close the block
        unclosed = f"~~~~phase60-ruling\n{body}\n```\n~~~\n\n```owner-quote\n{QUOTE}\n```\n"
        with self.assertRaises(ruling.RulingError):
            parse4(unclosed)

    def test_triple_backticks_inside_a_line_of_prose_are_not_a_fence(self):
        prose = ("```code``` is inline code that starts a line.\n"
                 "``` phase60-ruling ``` is not a fence either.\n"
                 "Write ```code``` inline in the middle of a line.\n")
        text = checkpoint4("continue", "120", prose=prose)
        self.assertEqual(parse4(text)["approved_first_omega_0"], 120.0)

    def test_a_longer_fence_of_the_other_character_does_not_close_a_block(self):
        text = ("~~~phase60-ruling\nruling: checkpoint-4\nanswer: go-to-verdict\n````\n\n"
                f"```owner-quote\n{QUOTE}\n```\n")
        with self.assertRaises(ruling.RulingError):
            parse4(text)

    def test_an_opening_fence_indented_four_spaces_is_not_a_fence(self):
        text = ("    ```phase60-ruling\nruling: checkpoint-4\nanswer: go-to-verdict\n```\n\n"
                f"```owner-quote\n{QUOTE}\n```\n")
        with self.assertRaises(ruling.RulingError):
            parse4(text)

    def test_an_unclosed_block_is_refused(self):
        with self.assertRaises(ruling.RulingError):
            parse4(f"```phase60-ruling\nruling: checkpoint-4\nanswer: go-to-verdict\n\n```owner-quote\n{QUOTE}\n```\n")
        with self.assertRaises(ruling.RulingError):
            parse4(checkpoint4("go-to-verdict", None) + "\n```text\nnever closed\n")

    def test_crlf_and_lone_cr_line_endings_are_accepted(self):
        text = checkpoint4("continue", "120")
        for ending in ("\r\n", "\r"):
            with self.subTest(ending=repr(ending)):
                self.assertEqual(parse4(text.replace("\n", ending))["approved_first_omega_0"], 120.0)

    def test_unicode_line_separators_do_not_split_lines(self):
        quote = "first line\u2028```phase60-ruling\u2028ruling: checkpoint-4\u2028answer: go-to-verdict\u2028```"
        parsed = parse4(checkpoint4("continue", "120", quote=quote))
        self.assertEqual(parsed["answer"], "continue")

    def test_an_unknown_kind_is_a_value_error(self):
        with self.assertRaises(ValueError):
            ruling.parse_machine_block(checkpoint4(), kind="checkpoint-5")

    def test_prose_outside_the_blocks_is_ignored(self):
        text = checkpoint4("continue", "120", prose="answer: go-to-verdict\nreading: rescue\n")
        self.assertEqual(parse4(text)["answer"], "continue")


class OpaqueQuoteTests(unittest.TestCase):
    BASELINE = {"answer": "continue", "approved_first_omega_0": 120.0}
    HOSTILE = (
        ("a fake machine block inside a tilde-fenced quote", "~~~~~~",
         "```phase60-ruling\nruling: checkpoint-4\nanswer: go-to-verdict\n```"),
        ("shorter fences inside a longer backtick fence", "`````",
         "```phase60-ruling\nruling: checkpoint-4\nanswer: go-to-verdict\n```\n"
         "````owner-quote\nx\n````"),
        ("the words of an answer", "```", "answer: go-to-verdict\napproved_first_omega_0: 9999"),
        ("a path", "```", "/etc/passwd ../../../secrets C:\\Windows\\System32"),
        ("a shell command", "```", "$(touch SENTINEL) `touch SENTINEL`; rm -rf / # nothing runs"),
        ("python text", "```", "__import__('os').system('touch SENTINEL'); eval('1+1')"),
        ("markdown structure", "```", "# Heading\n---\n> block quote\n| a | b |"),
        ("a very long line", "```", "x" * 100000),
    )

    def test_a_hostile_quote_changes_nothing_the_parser_returns(self):
        for label, fence, quote in self.HOSTILE:
            with self.subTest(case=label):
                text = checkpoint4("continue", "120", quote=quote, quote_fence=fence)
                self.assertEqual(parse4(text), self.BASELINE)
                text = checkpoint4("continue", "120", quote=quote, quote_fence=fence,
                                   quote_first=True)
                self.assertEqual(parse4(text), self.BASELINE)

    def test_exactly_one_quote_block_is_required(self):
        machine = "```phase60-ruling\nruling: checkpoint-4\nanswer: go-to-verdict\n```\n"
        with self.assertRaises(ruling.RulingError):
            parse4(machine)
        with self.assertRaises(ruling.RulingError):
            parse4(machine + f"\n```owner-quote\n{QUOTE}\n```\n\n```owner-quote\nagain\n```\n")

    def test_a_quote_that_closes_its_own_fence_early_is_refused_not_trusted(self):
        for label, quote in (
            ("then a second machine block",
             "```\n```phase60-ruling\nruling: checkpoint-4\nanswer: go-to-verdict\n```"),
            ("then a second quote opener", "```\n```owner-quote\nmore\n```"),
            ("then stray text", "before\n```\nanswer: go-to-verdict\n"),
        ):
            with self.subTest(case=label):
                with self.assertRaises(ruling.RulingError):
                    parse4(checkpoint4("continue", "120", quote=quote))

    def test_the_loaded_value_never_carries_the_quote(self):
        with tempfile.TemporaryDirectory(prefix="phase60-ruling-") as tmp:
            root = Path(tmp).resolve()
            init_repo(root)
            target = root / PHASE_REL / "60-CHECKPOINT-4-RULING.md"
            target.parent.mkdir(parents=True)
            marker = "UNIQUE-QUOTE-MARKER-7731"
            target.write_text(checkpoint4("continue", "120", quote=marker), encoding="utf-8")
            commit_all(root, "ruling")
            loaded = ruling.load_checkpoint4_ruling(repo_root=root)
            self.assertNotIn(marker, repr(loaded))
            self.assertEqual([f.name for f in dataclasses.fields(loaded)],
                             ["answer", "approved_first_omega_0", "sha256", "path"])

    def test_nothing_in_the_file_reaches_a_command_or_a_path(self):
        with tempfile.TemporaryDirectory(prefix="phase60-ruling-") as tmp:
            root = Path(tmp).resolve()
            init_repo(root)
            sentinel = root / "SENTINEL"
            quote = f"$(touch {sentinel}) `touch {sentinel}` ; touch {sentinel} ; {root}/../x"
            target = root / PHASE_REL / "60-CHECKPOINT-4-RULING.md"
            target.parent.mkdir(parents=True)
            target.write_text(checkpoint4("continue", "120", quote=quote), encoding="utf-8")
            commit_all(root, "ruling")
            calls = []
            real_run = subprocess.run

            def spy(*args, **kwargs):
                calls.append((args, kwargs))
                return real_run(*args, **kwargs)

            with mock.patch.object(ruling.subprocess, "run", spy):
                loaded = ruling.load_checkpoint4_ruling(repo_root=root)
            self.assertEqual(loaded.approved_first_omega_0, 120.0)
            self.assertFalse(sentinel.exists())
            self.assertGreaterEqual(len(calls), 2)
            for args, kwargs in calls:
                argv = args[0]
                self.assertIsInstance(argv, list)
                self.assertEqual(argv[0], "git")
                self.assertIs(kwargs.get("shell", False), False)
                for item in argv:
                    for forbidden in ("touch", "continue", "120", "approved", "SENTINEL"):
                        self.assertNotIn(forbidden, item)
            self.assertIn(loaded.path, [a for args, _ in calls for a in args[0]])


class CommittedTests(unittest.TestCase):
    def repo(self):
        tmp = tempfile.TemporaryDirectory(prefix="phase60-ruling-")
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name).resolve()
        init_repo(root)
        (root / "README.md").write_text("fixture\n")
        commit_all(root, "init")
        return root

    @staticmethod
    def put(root, text, name="60-CHECKPOINT-4-RULING.md"):
        target = root / PHASE_REL / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def test_a_clean_tracked_file_loads_with_its_sha256_and_relative_path(self):
        root = self.repo()
        target = self.put(root, checkpoint4("continue", "120"))
        commit_all(root, "ruling")
        loaded = ruling.load_checkpoint4_ruling(repo_root=root)
        self.assertEqual(loaded.answer, "continue")
        self.assertEqual(loaded.approved_first_omega_0, 120.0)
        self.assertEqual(loaded.sha256, hashlib.sha256(target.read_bytes()).hexdigest())
        self.assertEqual(loaded.path, (PHASE_REL / "60-CHECKPOINT-4-RULING.md").as_posix())
        with self.assertRaises(dataclasses.FrozenInstanceError):
            loaded.answer = "go-to-verdict"

    def test_an_untracked_file_is_refused(self):
        root = self.repo()
        self.put(root, checkpoint4("continue", "120"))
        with self.assertRaises(ruling.RulingError) as caught:
            ruling.load_checkpoint4_ruling(repo_root=root)
        self.assertIsInstance(caught.exception, ruling.RulingUncommitted)
        self.assertEqual(caught.exception.relative,
                         (PHASE_REL / "60-CHECKPOINT-4-RULING.md").as_posix())

    def test_a_tracked_file_with_an_uncommitted_change_is_refused(self):
        root = self.repo()
        target = self.put(root, checkpoint4("continue", "120"))
        commit_all(root, "ruling")
        target.write_text(checkpoint4("continue", "240"), encoding="utf-8")
        with self.assertRaises(ruling.RulingError):
            ruling.load_checkpoint4_ruling(repo_root=root)

    def test_a_staged_but_uncommitted_file_is_refused(self):
        root = self.repo()
        self.put(root, checkpoint4("continue", "120"))
        subprocess.run(["git", "add", "-A"], cwd=root, check=True, capture_output=True)
        with self.assertRaises(ruling.RulingUncommitted):
            ruling.load_checkpoint4_ruling(repo_root=root)

    def test_a_ruling_changed_and_recommitted_is_a_new_sha256(self):
        root = self.repo()
        self.put(root, checkpoint4("continue", "120"))
        commit_all(root, "first")
        first = ruling.load_checkpoint4_ruling(repo_root=root).sha256
        self.put(root, checkpoint4("continue", "240"))
        commit_all(root, "second")
        second = ruling.load_checkpoint4_ruling(repo_root=root)
        self.assertNotEqual(first, second.sha256)
        self.assertEqual(second.approved_first_omega_0, 240.0)

    def test_an_absent_file_is_refused_as_missing(self):
        root = self.repo()
        with self.assertRaises(ruling.RulingMissing):
            ruling.load_checkpoint4_ruling(repo_root=root)
        with self.assertRaises(ruling.RulingMissing):
            ruling.load_gap6009_ruling(repo_root=root)
        self.assertTrue(issubclass(ruling.RulingMissing, ruling.RulingError))

    def test_the_committed_check_can_be_waived_for_a_fixture(self):
        root = self.repo()
        self.put(root, checkpoint4("go-to-verdict", None))
        loaded = ruling.load_checkpoint4_ruling(repo_root=root, require_committed=False)
        self.assertEqual(loaded.answer, "go-to-verdict")
        self.assertIsNone(loaded.approved_first_omega_0)

    def test_an_explicit_test_path_inside_the_repository_is_read(self):
        root = self.repo()
        target = self.put(root, checkpoint4("continue", "60"), name="other.md")
        commit_all(root, "fixture")
        loaded = ruling.load_checkpoint4_ruling(repo_root=root, path=target)
        self.assertEqual(loaded.approved_first_omega_0, 60.0)
        relative = ruling.load_checkpoint4_ruling(repo_root=root, path=PHASE_REL / "other.md")
        self.assertEqual(relative.sha256, loaded.sha256)

    def test_a_path_outside_the_repository_is_refused(self):
        root = self.repo()
        with tempfile.TemporaryDirectory(prefix="phase60-outside-") as other:
            outside = Path(other) / "ruling.md"
            outside.write_text(checkpoint4("continue", "120"), encoding="utf-8")
            for waive in (True, False):
                with self.subTest(require_committed=not waive):
                    with self.assertRaises(ruling.RulingError):
                        ruling.load_checkpoint4_ruling(repo_root=root, path=outside,
                                                       require_committed=not waive)

    def test_a_symbolic_link_is_refused(self):
        root = self.repo()
        real = self.put(root, checkpoint4("continue", "120"), name="real.md")
        link = root / PHASE_REL / "60-CHECKPOINT-4-RULING.md"
        link.symlink_to(real)
        commit_all(root, "a link")
        with self.assertRaises(ruling.RulingError):
            ruling.load_checkpoint4_ruling(repo_root=root)

    def test_a_malformed_committed_file_is_refused(self):
        root = self.repo()
        self.put(root, checkpoint4("continue", "1e3"))
        commit_all(root, "bad value")
        with self.assertRaises(ruling.RulingError) as caught:
            ruling.load_checkpoint4_ruling(repo_root=root)
        self.assertNotIsInstance(caught.exception, (ruling.RulingMissing, ruling.RulingUncommitted))

    def test_a_file_that_is_not_utf8_is_refused(self):
        root = self.repo()
        target = root / PHASE_REL / "60-CHECKPOINT-4-RULING.md"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"\xff\xfe not text")
        commit_all(root, "bytes")
        with self.assertRaises(ruling.RulingError):
            ruling.load_checkpoint4_ruling(repo_root=root)

    def test_one_undecodable_byte_beside_a_valid_ruling_is_refused(self):
        root = self.repo()
        target = root / PHASE_REL / "60-CHECKPOINT-4-RULING.md"
        target.parent.mkdir(parents=True)
        target.write_bytes(checkpoint4("continue", "120").encode("utf-8") + b"\xff\n")
        commit_all(root, "a stray byte")
        with self.assertRaises(ruling.RulingError):
            ruling.load_checkpoint4_ruling(repo_root=root)

    def test_the_gap_60_09_loader_reads_its_own_fixed_file(self):
        root = self.repo()
        self.put(root, gap6009("rescue"), name="60-GAP-60-09-RULING.md")
        commit_all(root, "gap ruling")
        loaded = ruling.load_gap6009_ruling(repo_root=root)
        self.assertEqual(loaded.reading, "rescue")
        self.assertEqual(loaded.path, (PHASE_REL / "60-GAP-60-09-RULING.md").as_posix())
        self.assertEqual([f.name for f in dataclasses.fields(loaded)],
                         ["reading", "sha256", "path"])
        # the checkpoint 4 loader does not read the GAP-60-09 file, nor the reverse
        with self.assertRaises(ruling.RulingMissing):
            ruling.load_checkpoint4_ruling(repo_root=root)

    def test_the_gap_60_09_loader_refuses_a_checkpoint_4_block(self):
        root = self.repo()
        self.put(root, checkpoint4("continue", "120"), name="60-GAP-60-09-RULING.md")
        commit_all(root, "wrong kind")
        with self.assertRaises(ruling.RulingError):
            ruling.load_gap6009_ruling(repo_root=root)

    def test_the_fixed_paths_are_in_the_phase_directory(self):
        self.assertEqual(ruling.RULING4_REL, PHASE_REL / "60-CHECKPOINT-4-RULING.md")
        self.assertEqual(ruling.RULING_GAP6009_REL, PHASE_REL / "60-GAP-60-09-RULING.md")


class GridFactsTests(unittest.TestCase):
    @staticmethod
    def ruling_at(value, answer="continue"):
        return SimpleNamespace(answer=answer, approved_first_omega_0=value)

    def test_a_grid_value_that_equals_the_confirmed_setting(self):
        facts = ruling.ruling_grid_facts(self.ruling_at(120.0), scorecard=CARD,
                                         confirmed_first_omega_0=120.0)
        self.assertEqual(facts, {"on_grid": True, "equals_confirmed": True})

    def test_a_grid_value_that_is_not_the_confirmed_setting(self):
        facts = ruling.ruling_grid_facts(self.ruling_at(240.0), scorecard=CARD,
                                         confirmed_first_omega_0=120.0)
        self.assertEqual(facts, {"on_grid": True, "equals_confirmed": False})

    def test_a_value_off_the_grid_is_accepted_and_recorded(self):
        facts = ruling.ruling_grid_facts(self.ruling_at(37.5), scorecard=CARD,
                                         confirmed_first_omega_0=120.0)
        self.assertEqual(facts, {"on_grid": False, "equals_confirmed": False})

    def test_the_locked_value_is_not_on_the_sweep_grid(self):
        facts = ruling.ruling_grid_facts(self.ruling_at(30.0), scorecard=CARD,
                                         confirmed_first_omega_0=None)
        self.assertEqual(facts, {"on_grid": False, "equals_confirmed": False})

    def test_no_confirmed_setting_never_equals(self):
        facts = ruling.ruling_grid_facts(self.ruling_at(120.0), scorecard=CARD,
                                         confirmed_first_omega_0=None)
        self.assertEqual(facts, {"on_grid": True, "equals_confirmed": False})

    def test_the_grid_is_read_from_the_scorecard(self):
        stand_in = SimpleNamespace(section=lambda name: {"grid": [10.0, 20.0]})
        facts = ruling.ruling_grid_facts(self.ruling_at(20.0), scorecard=stand_in,
                                         confirmed_first_omega_0=20.0)
        self.assertEqual(facts, {"on_grid": True, "equals_confirmed": True})

    def test_only_a_continue_ruling_names_a_setting(self):
        for bad in (self.ruling_at(None, "go-to-verdict"), self.ruling_at(None),
                    self.ruling_at(120.0, "go-to-verdict")):
            with self.subTest(ruling=bad):
                with self.assertRaises(ruling.RulingError):
                    ruling.ruling_grid_facts(bad, scorecard=CARD, confirmed_first_omega_0=120.0)


class ModuleContractTests(unittest.TestCase):
    """The loader never executes, evaluates or imports anything from a ruling file."""

    @classmethod
    def setUpClass(cls):
        cls.source = Path(ruling.__file__).read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source)

    def test_no_dynamic_execution_and_no_shell(self):
        banned_builtins = {"eval", "exec", "compile", "__import__"}
        banned_attributes = {"system", "popen", "exec_module", "load_module"}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name):
                    self.assertNotIn(func.id, banned_builtins, node.lineno)
                elif isinstance(func, ast.Attribute):
                    self.assertNotIn(func.attr, banned_attributes, node.lineno)
                for keyword in node.keywords:
                    if keyword.arg == "shell":
                        self.assertFalse(
                            isinstance(keyword.value, ast.Constant) and keyword.value.value is True
                        )
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.name for alias in node.names] + [getattr(node, "module", "") or ""]
                self.assertFalse([n for n in names if n.split(".")[0] in {"importlib", "pickle", "yaml"}])

    def test_the_module_does_not_import_the_runner_the_trainer_or_the_evaluator(self):
        names = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.add(node.module or "")
        self.assertFalse([n for n in names if n.endswith("learnability_run")], names)
        self.assertFalse([n for n in names if n.startswith(("pinn.train", "pinn.evaluate"))], names)


if __name__ == "__main__":
    unittest.main()
