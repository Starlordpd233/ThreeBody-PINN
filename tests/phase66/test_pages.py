"""Plan 66-02 (EXP-01): the fenced-block and digit-boundary page helpers.

Module-level helpers the Phase 66 page tests reuse (their real-file classes
land in plan 66-03, once the pages exist): ``extract_block`` returns the one
fenced code block carrying a given info string and refuses zero or several,
``has_number`` matches a number as a standalone decimal token so ``0.01`` is
not found inside ``0.010856`` (the Phase 64 digit-boundary precedent), and
:class:`PageHelperTests` proves both on synthetic pages plus the design-block
equality a page's ``exp01-design`` block must satisfy against
``exp01_design()``.
"""

from __future__ import annotations

import json
import re
import unittest

from pinn.verification import diagnostic_phase66 as p66

_FENCE = re.compile(
    r"^```(?P<info>[^\n`]*)\n(?P<body>.*?)^```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)


def extract_block(text, info_string):
    """The body of the single fenced block named by ``info_string``.

    The info string is matched against the fence's final whitespace-separated
    token, so a JSON-labelled block (`` ```json exp01-design ``) is addressed
    by its name. Raises ``ValueError`` when the text carries zero or several
    such blocks, so a page cannot slip two competing design blocks past a test.
    """
    matches = [
        fence.group("body")
        for fence in _FENCE.finditer(text)
        if fence.group("info").split()[-1:] == [info_string]
    ]
    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one fenced {info_string!r} block, found {len(matches)}"
        )
    return matches[0]


def has_number(text, number):
    """Whether ``number`` appears as a standalone decimal token in ``text``.

    Digit-boundary matching: the token must not sit inside a longer number, so
    ``0.01`` is not found inside ``0.010856`` (nor ``157065`` inside
    ``1570650``), while a sentence period after the token still matches.
    """
    token = repr(number)
    pattern = re.compile(r"(?<![0-9.])" + re.escape(token) + r"(?!\.?[0-9])")
    return pattern.search(text) is not None


class PageHelperTests(unittest.TestCase):
    """The synthetic page-helper contract."""

    def test_extract_block_finds_exactly_one_fenced_block(self):
        page = (
            "# page\n\n"
            "```json exp01-design\n"
            '{"experiment": "EXP-01"}\n'
            "```\n\n"
            "```text\nnot a match\n```\n"
        )
        self.assertEqual(
            extract_block(page, "exp01-design"), '{"experiment": "EXP-01"}\n'
        )
        self.assertEqual(extract_block(page, "text"), "not a match\n")
        with self.assertRaises(ValueError):
            extract_block(page, "missing-block")
        doubled = page + "\n```json exp01-design\n{}\n```\n"
        with self.assertRaises(ValueError):
            extract_block(doubled, "exp01-design")

    def test_has_number_respects_digit_boundaries(self):
        self.assertFalse(has_number("movement 0.010856 grew", 0.01))
        self.assertTrue(has_number("the growth bar stays 0.01.", 0.01))
        self.assertTrue(has_number("min_growth is 0.01 exactly", 0.01))
        self.assertTrue(has_number("movement 0.010856 grew", 0.010856))
        self.assertTrue(has_number("bound 1.00001 here", 1.00001))
        self.assertFalse(has_number("bound 1.000012 here", 1.00001))
        self.assertTrue(has_number("steps 157065", 157065))
        self.assertFalse(has_number("steps 1570650", 157065))

    def test_a_design_block_must_equal_exp01_design(self):
        design_text = json.dumps(p66.exp01_design(), indent=2, sort_keys=True)
        page = f"# page\n\n```json exp01-design\n{design_text}\n```\n"
        self.assertEqual(
            json.loads(extract_block(page, "exp01-design")), p66.exp01_design()
        )
        # One digit changed anywhere in the block breaks the equality.
        tampered_text = design_text.replace("157065", "157066", 1)
        self.assertNotEqual(tampered_text, design_text)
        tampered = f"# page\n\n```json exp01-design\n{tampered_text}\n```\n"
        self.assertNotEqual(
            json.loads(extract_block(tampered, "exp01-design")),
            p66.exp01_design(),
        )


if __name__ == "__main__":
    unittest.main()
