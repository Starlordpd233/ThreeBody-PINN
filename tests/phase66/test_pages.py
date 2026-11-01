"""Plan 66-02/66-03 (EXP-01): page helpers and the real-file page tests.

Module-level helpers (``extract_block`` returns the one fenced code block
carrying a given info string and refuses zero or several, ``has_number``
matches a number as a standalone decimal token so ``0.01`` is not found inside
``0.010856``, the Phase 64 digit-boundary precedent) plus :class:
`PageHelperTests` on synthetic pages, and — since plan 66-03 committed the
pages — the real-file classes: :class:`TimingPageTests` ties the committed
timing page and its registration to ``exp01_design()``, the frozen settings,
the predicted band edges and the seven code digests, and (plan 66-03 task 3)
:class:`PredictionPageTests` and :class:`ExperimentRegistrationTests` do the
same for the full prediction page and the three experiment registrations.
"""

from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path

from pinn.verification import diagnostic_phase66 as p66

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PHASE_DIR = _REPO_ROOT / ".planning/phases/66-small-network-control"
_TIMING_PAGE = _PHASE_DIR / "66-TIMING-PREDICTION.md"
_TIMING_REGISTRATION = _PHASE_DIR / "evidence/timing/timing-registration.json"
_SMOKE_REGISTRATION = (
    _REPO_ROOT
    / ".planning/phases/65-probe-on-the-record-fit-harness"
    / "evidence/fit/smoke-registration.json"
)

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


class TimingPageTests(unittest.TestCase):
    """The committed timing page and registration carry the frozen design.

    Real-file tests (plan 66-03): the page's design block equals
    ``exp01_design()`` exactly, the predicted band edges and the reading
    rule's numbers appear at full precision, the registration pins the page
    bytes by SHA-256 and the seven live code digests, and the copied blocks
    equal the Phase 65 smoke registration's.
    """

    @classmethod
    def _page_text(cls):
        return _TIMING_PAGE.read_text()

    @classmethod
    def _registration(cls):
        return json.loads(_TIMING_REGISTRATION.read_bytes().decode("utf-8"))

    def test_the_design_block_equals_exp01_design(self):
        block = extract_block(self._page_text(), "exp01-design")
        self.assertEqual(json.loads(block), p66.exp01_design())

    def test_the_predicted_band_edges_and_rule_numbers_appear(self):
        text = self._page_text()
        for edge in (
            1.0961487784542576,
            1.211532860396811,
            1.1720120231532487,
            1.2953817098009592,
        ):
            self.assertTrue(has_number(text, edge), f"missing band edge {edge!r}")
        self.assertTrue(has_number(text, 0.01), "missing the 0.01 growth bar")
        self.assertTrue(has_number(text, p66.first_layer_frequency_bound(1000.0)))
        self.assertIn("three quarters of the run", text)
        self.assertIn("No rule is re-set after a result is seen.", text)

    def test_the_suspect_table_and_unsettled_reading_are_stated(self):
        text = self._page_text()
        self.assertIn("Under-training", text)
        self.assertIn("unsettled", text)
        self.assertIn("This does not show where the fault is", text)
        # The GAP-59-08 sentence, verbatim.
        self.assertIn(
            "eps_h here is the frozen scorer's autograd-velocity value on the "
            "gold grid; it is not the production gate's finite-difference "
            "value, GAP-59-08 (owner-routed, Phase 68) is open, and eps_h does "
            "not measure correctness for a near-constant predictor.",
            text,
        )

    def test_the_registration_pins_the_page_bytes(self):
        doc = self._registration()
        page_bytes = _TIMING_PAGE.read_bytes()
        self.assertEqual(
            hashlib.sha256(page_bytes).hexdigest(), doc["page"]["sha256"]
        )
        self.assertEqual(
            doc["page"]["path"],
            ".planning/phases/66-small-network-control/66-TIMING-PREDICTION.md",
        )

    def test_every_frozen_setting_equals_the_registration(self):
        doc = self._registration()
        settings = doc["settings"]
        self.assertEqual(settings["variant"], p66.EXP01_VARIANT.to_json_dict())
        self.assertEqual(settings["variant_registry"], "phase66")
        self.assertEqual(settings["seed"], 42)
        self.assertEqual(settings["runtime"], {"dtype": "float32", "device": "mps"})
        self.assertEqual(settings["orbit_key"], "hierarchical/gold/1632")
        self.assertEqual(settings["physical_window"], {"t_start": 0.0, "t_end": 10.0})
        self.assertEqual(settings["optimizer_steps"], 5200)
        self.assertEqual(settings["warmup_steps"], 200)
        self.assertEqual(settings["measured_steps"], 5000)
        self.assertEqual(
            settings["measured_steps"], settings["optimizer_steps"] - settings["warmup_steps"]
        )
        self.assertEqual(
            settings["similarity_cadence"], [0, 1300, 2600, 3900, 5200]
        )
        self.assertEqual(settings["loss_trace_stride"], 1)
        self.assertEqual(settings["whole_run_cap_seconds"], 600)
        self.assertEqual(settings["optimizer"]["kind"], "adam_constant_rate")
        self.assertEqual(settings["optimizer"]["lr"], 0.0001)
        self.assertEqual(settings["loss"]["kind"], "data_only")
        for key in ("mechanical_pass", "incomplete", "out_of_branch"):
            self.assertTrue(settings["reading_rule"][key], key)

    def test_the_code_dependencies_are_exactly_the_seven_live_files(self):
        doc = self._registration()
        expected_paths = [
            "pinn/verification/diagnostic_fit.py",
            "pinn/verification/diagnostic_guard.py",
            "pinn/verification/diagnostic_data.py",
            "pinn/verification/diagnostic_variants.py",
            "pinn/verification/diagnostic_similarity.py",
            "pinn/verification/diagnostic_phase66.py",
            "pinn/verification/diagnostic_power.py",
        ]
        self.assertEqual([entry["path"] for entry in doc["code_dependencies"]], expected_paths)
        for entry in doc["code_dependencies"]:
            live = hashlib.sha256((_REPO_ROOT / entry["path"]).read_bytes()).hexdigest()
            self.assertEqual(live, entry["sha256"], entry["path"])

    def test_the_copied_blocks_equal_the_smoke_registration(self):
        doc = self._registration()
        smoke = json.loads(_SMOKE_REGISTRATION.read_bytes().decode("utf-8"))
        for key in ("logger_parity", "context", "frozen", "pinned"):
            self.assertEqual(doc[key], smoke[key], key)


if __name__ == "__main__":
    unittest.main()
