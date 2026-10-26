"""Phase 60 (SPEC Requirement 1, GAP-60-01): the scope amendment matches the SPEC.

In plain language: ``60-SPEC.md`` holds six short paragraphs that say what the
requirement files must say about the data-only arms, the Rung 2 skip and the
hard-stage probes. This module reads those paragraphs from the SPEC itself and
checks that each one appears, word for word, in the one section of
``REQUIREMENTS.md`` or ``ROADMAP.md`` it is meant for. It also checks that the
frozen scorecard did not move, so the written rules and the pre-registered
numbers stay consistent.

The comparison is the one GAP-60-01 chose (option A): both sides go through
Unicode NFC normalization and whitespace collapse, and nothing else. Markdown
emphasis and backticks are not stripped, so a stray ``**`` or a lost backtick
makes a paragraph fail. Containment is tested inside the paragraph's own
section, never in the whole file, because the roadmap sentence also ends the
Gate G2 paragraph and would otherwise pass for the wrong reason.

``LocatorSelfTests`` prove that the comparison and the locators cannot pass
vacuously. ``ScorecardFrozenTests`` repeat the Phase 59 freeze checks.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import unicodedata
import unittest
from pathlib import Path

from pinn.verification.feasibility_scorecard import SCORECARD_SHA256, load_scorecard

ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / ".planning" / "phases" / "60-single-system-learnability" / "60-SPEC.md"
# The v2.4 close archived the live requirements and roadmap with the same v2.4 text.
REQUIREMENTS_PATH = ROOT / ".planning" / "milestones" / "v2.4-REQUIREMENTS.md"
ROADMAP_PATH = ROOT / ".planning" / "milestones" / "v2.4-ROADMAP.md"
SCORECARD_PATH = ROOT / "pinn" / "verification" / "artifacts" / "feasibility_scorecard_v1.json"
PHASE59_VERIFIER = (
    ROOT
    / ".planning"
    / "phases"
    / "59-read-only-baseline-scorecard"
    / "evidence"
    / "verify_phase59_evidence.py"
)

FROZEN_SCORECARD_SHA256 = "f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b"
AMENDMENT_HEADING = "## Amendment text"

# The six labels, in the order the SPEC lists them. U+2463 is CIRCLED DIGIT FOUR.
SCOPE_39 = "SCOPE-39"
FEAS_04 = "FEAS-04, last acceptance bullet"
ROADMAP_3 = "Roadmap success criterion 3, added sentence"
FEAS_09 = "FEAS-09"
SCOPE_44 = "SCOPE-44"
CHECKPOINT_4 = "Checkpoint ④ continue"
LABELS = (SCOPE_39, FEAS_04, ROADMAP_3, FEAS_09, SCOPE_44, CHECKPOINT_4)


class SourceMiss(AssertionError):
    """A source file lacks the shape this check expects, so it cannot be located."""


def collapse(text: str) -> str:
    """NFC-normalize, then collapse every whitespace run to one space (GAP-60-01)."""
    return " ".join(unicodedata.normalize("NFC", text).split())


def contains(section: str, paragraph: str) -> bool:
    return collapse(paragraph) in collapse(section)


def _only(items: list, what: str):
    if len(items) != 1:
        raise SourceMiss(f"expected exactly one {what}, found {len(items)}")
    return items[0]


def _first_index(lines: list[str], begin: int, stop: int, prefix: str, what: str) -> int:
    for index in range(begin, stop):
        if lines[index].startswith(prefix):
            return index
    raise SourceMiss(f"{what} not found")


# ---------------------------------------------------------------------------
# The SPEC parser: the single source of truth for the six paragraphs.
# ---------------------------------------------------------------------------

_PARAGRAPH = re.compile(r"\*\*(?P<label>[^*\n]+?)\.\*\*[ \t]*(?P<body>.+)", re.DOTALL)


def parse_amendment(spec_text: str) -> dict[str, str]:
    """Return label -> body for each bold-labelled paragraph under the heading.

    The section runs from the "## Amendment text" line to the next line that
    starts with "## ". A block with no bold label (the "Compare after collapsing
    whitespace." line) is not a paragraph.
    """
    lines = spec_text.splitlines()
    start = _only(
        [i for i, line in enumerate(lines) if line.rstrip() == AMENDMENT_HEADING],
        f"{AMENDMENT_HEADING!r} heading",
    )
    stop = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines)
    )
    blocks = re.split(r"\n\s*\n", "\n".join(lines[start + 1 : stop]).strip())
    found: dict[str, str] = {}
    for block in blocks:
        match = _PARAGRAPH.match(block.strip())
        if match is None:
            continue
        label = match["label"]
        if label in found:
            raise SourceMiss(f"amendment label {label!r} appears twice")
        found[label] = match["body"].strip()
    return found


# ---------------------------------------------------------------------------
# Section locators. Each returns the raw text of exactly one designated section.
# ---------------------------------------------------------------------------

_HEADING = re.compile(r"#{1,6}\s")


def requirements_row(text: str, row_id: str) -> str:
    """The one table row that begins "| <row_id> |"."""
    prefix = f"| {row_id} |"
    return _only(
        [line for line in text.splitlines() if line.startswith(prefix)],
        f"table row for {row_id}",
    )


def requirements_entry(text: str, entry_id: str, next_id: str) -> str:
    """The checkbox item for ``entry_id`` up to the line before ``next_id``'s item."""
    lines = text.splitlines()

    def item(identifier: str) -> int:
        pattern = re.compile(rf"- \[[ xX]\] \*\*{re.escape(identifier)}\*\*")
        return _only(
            [i for i, line in enumerate(lines) if pattern.match(line)],
            f"checkbox item for {identifier}",
        )

    start, end = item(entry_id), item(next_id)
    if end <= start:
        raise SourceMiss(f"{next_id} does not follow {entry_id}")
    return "\n".join(lines[start:end])


def roadmap_criterion_3(text: str) -> str:
    """Success criterion 3 of the "### Phase 60:" section, and nothing around it."""
    lines = text.splitlines()
    start = _only(
        [i for i, line in enumerate(lines) if line.startswith("### Phase 60:")],
        "Phase 60 heading",
    )
    stop = next(
        (i for i in range(start + 1, len(lines)) if _HEADING.match(lines[i])), len(lines)
    )
    criteria = _first_index(lines, start, stop, "**Success Criteria**", "success-criteria line")
    first = _first_index(lines, criteria, stop, "  3. ", "criterion 3")
    last = _first_index(lines, first + 1, stop, "  4. ", "criterion 4")
    return "\n".join(lines[first:last])


def owner_checkpoint_4(text: str) -> str:
    """Item 4 of "## Owner Checkpoints", up to the next blank line."""
    lines = text.splitlines()
    heading = _only(
        [i for i, line in enumerate(lines) if line.startswith("## Owner Checkpoints")],
        "Owner Checkpoints heading",
    )
    stop = next(
        (i for i in range(heading + 1, len(lines)) if lines[i].startswith("## ")), len(lines)
    )
    item = _first_index(lines, heading + 1, stop, "4. **A G2 sweep rescue", "checkpoint 4 item")
    end = next((i for i in range(item, stop) if not lines[i].strip()), stop)
    return "\n".join(lines[item:end])


SECTIONS = {
    SCOPE_39: (REQUIREMENTS_PATH, lambda text: requirements_row(text, "SCOPE-39")),
    FEAS_04: (REQUIREMENTS_PATH, lambda text: requirements_entry(text, "FEAS-04", "FEAS-05")),
    ROADMAP_3: (ROADMAP_PATH, roadmap_criterion_3),
    FEAS_09: (REQUIREMENTS_PATH, lambda text: requirements_entry(text, "FEAS-09", "FEAS-10")),
    SCOPE_44: (REQUIREMENTS_PATH, lambda text: requirements_row(text, "SCOPE-44")),
    CHECKPOINT_4: (REQUIREMENTS_PATH, owner_checkpoint_4),
}


def section_text(label: str) -> str:
    path, locate = SECTIONS[label]
    return locate(path.read_text(encoding="utf-8"))


def read_amendment() -> dict[str, str]:
    return parse_amendment(SPEC_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Tests.
# ---------------------------------------------------------------------------


class ParserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.amendment = read_amendment()

    def test_exactly_the_six_labels_are_found(self):
        self.assertEqual(sorted(self.amendment), sorted(LABELS))
        self.assertEqual(len(self.amendment), 6)

    def test_every_body_is_non_empty(self):
        for label, body in self.amendment.items():
            with self.subTest(label=label):
                self.assertTrue(collapse(body))

    def test_the_leading_instruction_line_is_not_a_paragraph(self):
        for body in self.amendment.values():
            self.assertNotIn("Compare after collapsing whitespace.", body)

    def test_checkpoint_paragraph_keeps_its_circled_digit_and_backticks(self):
        label = _only([name for name in self.amendment if name.startswith("Checkpoint")], "label")
        self.assertIn("④", label)
        body = self.amendment[label]
        self.assertIn("`first_omega_0`", body)
        self.assertIn("`pinn_architecture.md`", body)

    def test_parser_stops_at_the_next_heading_and_skips_unlabelled_blocks(self):
        text = "\n".join(
            [
                "## Before",
                "**Early.** Not part of the section.",
                "",
                AMENDMENT_HEADING,
                "",
                "Compare after collapsing whitespace.",
                "",
                "**Kept.** First line of the body",
                "continues on a second line.",
                "",
                "## After",
                "**Late.** Also not part of the section.",
            ]
        )
        self.assertEqual(
            parse_amendment(text), {"Kept": "First line of the body\ncontinues on a second line."}
        )

    def test_parser_refuses_a_missing_heading_and_a_repeated_label(self):
        with self.assertRaises(SourceMiss):
            parse_amendment("## Something else\n**A.** text\n")
        with self.assertRaises(SourceMiss):
            parse_amendment(f"{AMENDMENT_HEADING}\n\n**A.** one\n\n**A.** two\n")


class ContainmentTests(unittest.TestCase):
    """Each SPEC paragraph appears, after NFC and whitespace collapse, in its own section."""

    @classmethod
    def setUpClass(cls):
        cls.amendment = read_amendment()

    def _assert_contained(self, label: str) -> None:
        path, _locate = SECTIONS[label]
        self.assertTrue(
            contains(section_text(label), self.amendment[label]),
            f"{label}: the SPEC paragraph is not contained in its section of {path.name}\n"
            f"SPEC paragraph: {collapse(self.amendment[label])}\n"
            f"Section:        {collapse(section_text(label))}",
        )

    def test_scope_39_row(self):
        self._assert_contained(SCOPE_39)

    def test_feas_04_last_acceptance_bullet(self):
        self._assert_contained(FEAS_04)

    def test_roadmap_success_criterion_3_added_sentence(self):
        self._assert_contained(ROADMAP_3)

    def test_feas_09_entry(self):
        self._assert_contained(FEAS_09)

    def test_scope_44_row(self):
        self._assert_contained(SCOPE_44)

    def test_checkpoint_4_continue(self):
        self._assert_contained(CHECKPOINT_4)


class LocatorSelfTests(unittest.TestCase):
    """The comparison and the locators cannot pass vacuously."""

    @classmethod
    def setUpClass(cls):
        cls.amendment = read_amendment()

    def test_collapse_ignores_wrapping_and_composition_but_keeps_markdown(self):
        self.assertEqual(collapse("a\n   b\t c d"), "a b c d")
        self.assertEqual(collapse("é"), collapse("é"))
        self.assertNotEqual(collapse("**a** b"), collapse("a b"))
        self.assertNotEqual(collapse("`a` b"), collapse("a b"))

    def test_one_changed_word_breaks_containment(self):
        for label, body in self.amendment.items():
            with self.subTest(label=label):
                section = f"| {label} | An earlier sentence. {body} A later sentence. |"
                self.assertTrue(contains(section, body))
                words = body.split()
                words[len(words) // 2] += "x"
                changed = section.replace(body, " ".join(words))
                self.assertNotEqual(changed, section)
                self.assertFalse(contains(changed, body))

    def test_each_locator_returns_one_bounded_section(self):
        # label: (pattern the section must start with, text that must lie outside it)
        cases = {
            SCOPE_39: (r"\| SCOPE-39 \| ", ("\n", "| SCOPE-40 |")),
            FEAS_04: (r"- \[[ xX]\] \*\*FEAS-04\*\*: ", ("**FEAS-05**",)),
            ROADMAP_3: (
                r"  3\. Rung 2 has scored results",
                ("\n  4. ", "**Gate G2**", "Otherwise G2 did not fire"),
            ),
            FEAS_09: (r"- \[[ xX]\] \*\*FEAS-09\*\*: ", ("**FEAS-10**",)),
            SCOPE_44: (r"\| SCOPE-44 \| ", ("\n",)),
            CHECKPOINT_4: (r"4\. \*\*A G2 sweep rescue", ("\n\n", "Everything else proceeds")),
        }
        self.assertEqual(sorted(cases), sorted(LABELS))
        for label, (start, outside) in cases.items():
            with self.subTest(label=label):
                text = section_text(label)
                self.assertRegex(text, rf"\A{start}")
                for fragment in outside:
                    self.assertNotIn(fragment, text)

    def test_roadmap_locator_leaves_out_the_gate_g2_paragraph(self):
        roadmap = ROADMAP_PATH.read_text(encoding="utf-8")
        self.assertIn("Otherwise G2 did not fire", roadmap)
        located = collapse(roadmap_criterion_3(roadmap))
        self.assertEqual(located.count(collapse(self.amendment[ROADMAP_3])), 1)
        self.assertNotIn("Otherwise G2 did not fire", located)

    def test_roadmap_locator_ignores_a_copy_outside_criterion_3(self):
        sentence = self.amendment[ROADMAP_3]
        roadmap = "\n".join(
            [
                "### Phase 59: Earlier",
                "**Success Criteria** (what must be TRUE):",
                "  3. An earlier phase's item.",
                "  4. Another item.",
                "### Phase 60: Single-System Learnability",
                f"Otherwise G2 did not fire. {sentence}",
                "**Success Criteria** (what must be TRUE):",
                "  2. Second item.",
                "  3. Rung 2 has scored results.",
                "     - a wrapped sub-bullet",
                "  4. Gate G2 is evaluated.",
                "### Phase 61: Later",
                "**Success Criteria** (what must be TRUE):",
                "  3. A later phase's item.",
                "  4. Another later item.",
            ]
        )
        located = roadmap_criterion_3(roadmap)
        self.assertIn("Rung 2 has scored results.", located)
        self.assertIn("a wrapped sub-bullet", located)
        self.assertFalse(contains(located, sentence))
        self.assertNotIn("earlier phase", located)
        self.assertNotIn("later phase", located)

    def test_locators_refuse_a_missing_or_repeated_anchor(self):
        with self.assertRaises(SourceMiss):
            requirements_row("| SCOPE-40 | other row\n", "SCOPE-39")
        with self.assertRaises(SourceMiss):
            requirements_row("| SCOPE-39 | one\n| SCOPE-39 | two\n", "SCOPE-39")
        with self.assertRaises(SourceMiss):
            requirements_entry("- [ ] **FEAS-04**: only\n", "FEAS-04", "FEAS-05")
        with self.assertRaises(SourceMiss):
            requirements_entry(
                "- [ ] **FEAS-05**: after\n- [ ] **FEAS-04**: before\n", "FEAS-04", "FEAS-05"
            )
        with self.assertRaises(SourceMiss):
            owner_checkpoint_4("## Owner Checkpoints\n\n1. **First.** text\n")
        with self.assertRaises(SourceMiss):
            roadmap_criterion_3("### Phase 61: Later\n  3. Not phase 60\n  4. Neither\n")


class ScorecardFrozenTests(unittest.TestCase):
    """The frozen scorecard is byte-unchanged (SCOPE-42; SPEC Requirement 1)."""

    def test_bytes_match_the_frozen_hash(self):
        digest = hashlib.sha256(SCORECARD_PATH.read_bytes()).hexdigest()
        self.assertEqual(digest, SCORECARD_SHA256)
        self.assertEqual(digest, FROZEN_SCORECARD_SHA256)

    def test_the_strict_loader_accepts_the_file(self):
        self.assertEqual(load_scorecard().sha256, FROZEN_SCORECARD_SHA256)

    def test_the_phase_59_freeze_check_prints_its_ok_token(self):
        result = subprocess.run(
            [sys.executable, "-B", str(PHASE59_VERIFIER), "scorecard-frozen"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("SCORECARD-FROZEN-OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
