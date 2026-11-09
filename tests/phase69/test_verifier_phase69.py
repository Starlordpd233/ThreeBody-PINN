"""Reject false Phase 69 evidence without training or scoring data."""

import json
import contextlib
import copy
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
VERIFIER = ROOT / ".planning/phases/69-findings-redesign-decision/evidence/verify_phase69.py"


def load_verifier():
    spec = importlib.util.spec_from_file_location("verify_phase69", VERIFIER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SourceTracerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_verifier()

    def test_real_cli_connects_historical_failure_and_original_control(self):
        result = subprocess.run(
            [sys.executable, "-B", str(VERIFIER), "sources"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PHASE69-SOURCES-OK", result.stdout)
        report = json.loads(result.stdout.split("\nPHASE69-SOURCES-OK")[0])
        comparison = report["matched_comparisons"][0]
        self.assertEqual((comparison["system"], comparison["seed"]), (1632, 42))
        self.assertEqual(comparison["historical"]["adam_E"], 1.1606404574102112)
        self.assertEqual(comparison["historical"]["polish_E"], 1.157387378319295)
        self.assertEqual(comparison["historical"]["official_E"], 1.157387378319295)
        self.assertEqual(comparison["historical"]["tier"], 0)
        self.assertEqual(comparison["control"]["E"], 0.040691019043637484)
        self.assertEqual(comparison["control"]["tier"], 1)
        self.assertTrue(comparison["control"]["settled"])

    def test_altered_digest_and_missing_committed_object_are_rejected(self):
        m = self.module
        path = f"{m.P60}/evidence/arms/r1-1632/record.json"
        with self.assertRaisesRegex(m.VerifyError, "digest"):
            m.read_source(path, m.BASELINE, "0" * 64)
        with self.assertRaisesRegex(m.VerifyError, "unavailable"):
            m.read_source(path, "0" * 40)
        with self.assertRaisesRegex(m.VerifyError, "unavailable"):
            m.read_source(f"{m.P60}/evidence/missing.json", m.BASELINE)

    def test_original_registration_passes_and_current_substitution_fails(self):
        m = self.module
        sources = m.Sources()
        control = sources.json(f"{m.P67}/evidence/exp03/science/main-1632-s42/lr1e-4/record.json")
        original = m.publication_registration(control, m.CONTROL_PUBLICATIONS["main-1632-s42"], sources)
        self.assertIsInstance(original, dict)
        self.assertNotEqual(
            m.sha256(sources.read(control["registration"]["path"])),
            control["registration"]["sha256"],
        )
        with self.assertRaisesRegex(m.VerifyError, "digest"):
            m.publication_registration(control, m.BASELINE, sources)

    def test_changed_seed_or_case_is_rejected(self):
        m = self.module
        sources = m.Sources()
        old = sources.json(f"{m.P60}/evidence/arms/r1-1632/record.json")
        control = sources.json(f"{m.P67}/evidence/exp03/science/main-1632-s42/lr1e-4/record.json")
        review = sources.json(f"{m.P67}/evidence/exp03/review.json")
        changed = copy.deepcopy(control)
        changed["seed"] = 41
        with self.assertRaisesRegex(m.VerifyError, "mismatch"):
            m.matched_comparison("main-1632-s42", old, changed, review, sources)
        with self.assertRaisesRegex(m.VerifyError, "unknown case"):
            m.matched_comparison("main-1632-s41", old, control, review, sources)

    def test_corrupt_inventory_makes_cli_fail_without_success_marker(self):
        m = self.module
        altered = copy.deepcopy(m.load_inventory())
        altered["sources"]["source_rows"][0]["sha256"] = "0" * 64
        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(m, "load_inventory", return_value=altered):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                status = m.main(["sources"])
        self.assertEqual(status, 1)
        self.assertNotIn("PHASE69-SOURCES-OK", stdout.getvalue())
        self.assertIn("differs", stderr.getvalue())

    def test_json_boolean_cannot_substitute_for_numeric_tier(self):
        m = self.module
        altered = copy.deepcopy(m.load_inventory())
        altered["sources"]["matched_comparisons"][0]["control"]["tier"] = True
        with mock.patch.object(m, "load_inventory", return_value=altered):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(m.main(["sources"]), 1)

    def test_path_escape_and_non_evidence_paths_are_rejected(self):
        m = self.module
        for path in ("../outside.json", "/tmp/outside.json", "simulation_data/train.json",
                     f"{m.P67}/evidence/../review.json", f"{m.P67}/evidence/diagnostic.weights"):
            with self.subTest(path=path), self.assertRaises(m.VerifyError):
                m.read_source(path, m.BASELINE)


class IdentityAndCostTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_verifier()
        cls.sources = cls.module.build_sources()
        cls.cost = cls.module.build_cost()

    def test_complete_inventory_preserves_all_registered_experiments(self):
        report = self.sources
        self.assertEqual(len(report.get("experiments", {})), 9)
        self.assertEqual(len(report["matched_comparisons"]), 2)
        self.assertEqual(report["experiments"]["EXP-02"]["confirmed"], [])
        self.assertEqual(report["experiments"]["EXP-04"]["confirmed"], [])
        self.assertEqual(report["experiments"]["EXP-05"]["confirmed"], [])

    def test_real_cost_cli_reports_attempt_and_fit_wall_views_separately(self):
        result = subprocess.run(
            [sys.executable, "-B", str(VERIFIER), "cost"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout.split("\nPHASE69-COST-OK")[0])
        self.assertEqual(report["published_attempts"], 129)
        self.assertEqual(report["utc_seconds"], "107626")
        self.assertEqual(report["fit_wall_records"], 125)
        self.assertEqual(report["fit_wall_seconds"], "107582.1065162036579550")

    def test_repeat_roles_are_keyed_and_shuffled_order_changes_no_binding(self):
        exp = self.sources["experiments"]["EXP-03"]
        cells = exp["contrasts"]["lr1e-3"]["cases"]
        self.assertEqual(cells["repeat-1632-s41"]["relative_E_effect"], 39.16428044173176)
        self.assertEqual(cells["repeat-851-s42"]["relative_E_effect"], 15.376889578229147)
        rows = list(reversed(exp["arms"]))
        indexed = self.module.index_cases(rows)
        controls = {row["case"]: row for row in indexed.values() if row["arm"] == "lr1e-4"}
        self.assertEqual(controls["repeat-851-s42"]["score"]["E"], 0.09549573839491703)
        self.assertEqual(controls["repeat-1632-s41"]["score"]["E"], 0.03491785615016659)

    def test_equal_values_do_not_merge_distinct_cases_or_metric_routes(self):
        controls = [row for row in self.sources["experiments"]["EXP-03"]["arms"] if row["arm"] == "lr1e-4"]
        rows = copy.deepcopy(controls[:2])
        rows[1]["score"] = rows[0]["score"]
        self.assertEqual(len(self.module.index_cases(rows)), 2)
        another_route = copy.deepcopy(rows[0])
        another_route["metric_route"]["grid"] = "base"
        self.assertEqual(len(self.module.index_cases([rows[0], another_route])), 2)

    def test_duplicate_case_and_incorrect_role_are_rejected(self):
        m = self.module
        row = self.sources["experiments"]["EXP-03"]["arms"][0]
        with self.assertRaisesRegex(m.VerifyError, "duplicate"):
            m.index_cases([row, copy.deepcopy(row)])
        changed = copy.deepcopy(row)
        changed["role"] = "main" if row["role"] != "main" else "repeat-seed"
        with self.assertRaisesRegex(m.VerifyError, "mismatch"):
            m.index_cases([changed])

    def test_swapped_review_repeat_values_are_rejected(self):
        m = self.module
        read_json = m.Sources.json

        def altered(sources, path, *args, **kwargs):
            value = read_json(sources, path, *args, **kwargs)
            if path.endswith("exp03/review.json"):
                cases = value["contrasts"]["lr1e-3"]["cases"]
                cases["repeat-seed"], cases["repeat-system"] = cases["repeat-system"], cases["repeat-seed"]
            return value

        with mock.patch.object(m.Sources, "json", altered):
            with self.assertRaisesRegex(m.VerifyError, "mismatch"):
                m.build_sources()

    def test_repeated_control_references_count_one_attempt(self):
        m = self.module
        row = next(row for row in self.cost["activities"] if row["activity"] == "phase67-science")
        report = m.summarize_activities([row, copy.deepcopy(row), copy.deepcopy(row)])
        self.assertEqual(report["published_attempts"], 1)
        self.assertEqual(report["utc_seconds"], row["utc_seconds"])
        self.assertEqual(report["fit_wall_seconds"], row["fit_wall_seconds"])

    def test_conflicting_or_differently_named_duplicate_attempts_are_rejected(self):
        m = self.module
        row = self.cost["activities"][1]
        changed = copy.deepcopy(row)
        changed["utc_seconds"] = "999"
        with self.assertRaisesRegex(m.VerifyError, "conflicting"):
            m.summarize_activities([row, changed])
        changed = copy.deepcopy(row)
        changed["attempt"] += ".duplicate"
        with self.assertRaisesRegex(m.VerifyError, "duplicate"):
            m.summarize_activities([row, changed])

    def test_absent_duration_stays_unknown_and_partial_attempt_is_retained(self):
        m = self.module
        row = copy.deepcopy(next(row for row in self.cost["activities"] if row["activity"] == "phase67-science"))
        row.update(utc_seconds=None, fit_wall_seconds=None, status="incomplete")
        report = m.summarize_activities([row])
        self.assertEqual(report["attempts"], 1)
        self.assertEqual(report["published_attempts"], 0)
        self.assertEqual(report["unknown_utc_attempts"], 1)
        self.assertIsNone(report["utc_seconds"])
        self.assertIsNone(report["fit_wall_seconds"])
        self.assertIsNone(row["utc_seconds"])

    def test_invalid_duration_and_timestamp_refuse(self):
        m = self.module
        for value in ("-0.1", "NaN", "Infinity", "bad", True):
            with self.subTest(value=value), self.assertRaises(m.VerifyError):
                m.duration(value, "test")
        for start, end in (("2026-11-01T00:00:01+00:00", "2026-11-01T00:00:00+00:00"),
                           ("2026-11-01T00:00:00", "2026-11-01T00:00:01"), ("bad", "bad")):
            with self.subTest(start=start), self.assertRaises(m.VerifyError):
                m.utc_interval(start, end)
        self.assertIsNone(m.utc_interval(None, None))

    def test_timing_bases_and_yardstick_are_separate_views(self):
        report = self.cost
        self.assertEqual(report["summary"]["timed_attempts"], 129)
        self.assertEqual(report["named_activity_utc_subtotal"],
                         {"timed_activities": 130, "utc_seconds": "107626.594706"})
        self.assertEqual(report["yardstick_capture"]["utc_seconds"], "0.594706")
        self.assertEqual(report["yardstick_capture"]["elapsed_seconds"], "0.5945865410612896")
        probe = next(row for row in report["activities"] if row["activity"] == "phase65-probe")
        self.assertIsNone(probe["utc_seconds"])
        self.assertEqual(report["summary"]["unknown_probe_activities"], 1)
        self.assertTrue(any(row["below_timestamp_resolution"] for row in report["activities"]))

    def test_boundary_values_and_registered_unconfirmed_readings_survive(self):
        exp = self.sources["experiments"]["EXP-03"]
        self.assertEqual(exp["confirmed"], [{"arm": "lr1e-3", "confirmation": "confirmed-worsening"}])
        self.assertEqual(exp["contrasts"]["lr3e-5"]["confirmation"], "ambiguous")
        self.assertEqual(exp["contrasts"]["lr1e-5"]["confirmation"], "unsettled")
        self.assertEqual(self.sources["matched_comparisons"][1]["historical"]["polish_E"], 1.2383540710834968)
        self.assertEqual(self.sources["recipe"]["module_count"], 33)

    def test_changed_accounting_inventory_is_rejected(self):
        m = self.module
        altered = copy.deepcopy(m.load_inventory())
        altered["cost"]["summary"]["utc_seconds"] = "107627"
        with mock.patch.object(m, "load_inventory", return_value=altered):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(m.main(["cost"]), 1)


class TraceabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_verifier()

    def setUp(self):
        self.requirements = """# Requirements: v2.5 Example
## v2.5 Requirements
- [ ] **EXP-01**: first
- [x] **VER-23**: second
## Scope Boundaries
- [ ] **SCOPE-49**: excluded
## Future Requirements
- [ ] **FUT-01**: excluded
## Traceability
| Requirement | Phase | Status |
| EXP-01 | Phase 65 | Open |
| VER-23 | Phase 69 | Complete |
"""
        self.roadmap = """# Roadmap
## v2.5 Example
## Phase Details
### Phase 65: First
**Requirements**: EXP-01
### Phase 69: Second
**Requirements**: VER-23
## Progress
0/2 complete
## v2.4 Archived
## Phase Details
### Phase 60: Old
**Requirements**: OLD-01
"""
        self.phases = {"65", "69"}

    def report(self, requirements=None, roadmap=None):
        return self.module.traceability_report(
            self.requirements if requirements is None else requirements,
            self.roadmap if roadmap is None else roadmap,
            self.phases.__contains__,
        )

    def test_real_traceability_cli_checks_active_sources(self):
        result = subprocess.run([sys.executable, "-B", str(VERIFIER), "traceability"],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout.split("\nPHASE69-TRACEABILITY-OK")[0])
        self.assertTrue(report["valid"])
        self.assertEqual(report["definition_count"], report["table_count"])
        self.assertEqual(report["definition_count"], report["roadmap_count"])
        self.assertGreater(report["definition_count"], 0)

    def test_nonempty_active_inventory_excludes_scope_future_and_archive(self):
        report = self.report()
        self.assertEqual(report["definition_ids"], ["EXP-01", "VER-23"])
        self.assertEqual(report["mapped_phases"], ["65", "69"])
        self.assertEqual(report["definition_count"], 2)
        self.assertFalse(any(report["duplicate_ids"].values()))

    def test_row_definition_and_phase_order_do_not_change_mapping(self):
        requirements = self.requirements.replace(
            "- [ ] **EXP-01**: first\n- [x] **VER-23**: second",
            "- [x] **VER-23**: second\n- [ ] **EXP-01**: first",
        ).replace("| EXP-01 | Phase 65 | Open |\n| VER-23 | Phase 69 | Complete |",
                  "| VER-23 | Phase 69 | Complete |\n| EXP-01 | Phase 65 | Open |")
        roadmap = self.roadmap.replace(
            "### Phase 65: First\n**Requirements**: EXP-01\n### Phase 69: Second\n**Requirements**: VER-23",
            "### Phase 69: Second\n**Requirements**: VER-23\n### Phase 65: First\n**Requirements**: EXP-01",
        )
        self.assertEqual(self.report(requirements, roadmap)["mappings"], self.report()["mappings"])

    def test_valid_new_requirement_and_phase_need_no_code_change(self):
        requirements = self.requirements.replace("## Scope Boundaries", "- [ ] **EXP-06**: extra\n## Scope Boundaries")
        requirements += "| EXP-06 | Phase 70 | Pending |\n"
        roadmap = self.roadmap.replace("## Progress", "### Phase 70: Added\n**Requirements**: EXP-06\n## Progress")
        self.phases.add("70")
        report = self.report(requirements, roadmap)
        self.assertEqual(report["definition_count"], 3)
        self.assertEqual(report["mapped_phases"], ["65", "69", "70"])

    def test_completion_status_does_not_determine_mapping(self):
        requirements = self.requirements.replace("[ ]", "[x]").replace("Complete", "Pending").replace("Open", "Complete")
        roadmap = self.roadmap.replace("0/2 complete", "2/2 complete")
        changed = self.report(requirements, roadmap)
        before = self.report()
        for field in ("requirements_sha256", "roadmap_sha256"):
            changed.pop(field)
            before.pop(field)
        self.assertEqual(changed, before)

    def test_empty_and_missing_inventories_refuse(self):
        for requirements, roadmap in (("", ""), (self.requirements, ""),
                                      (self.requirements.replace("- [ ] **EXP-01**: first", "").replace("- [x] **VER-23**: second", ""), self.roadmap),
                                      (self.requirements.replace("| EXP-01 | Phase 65 | Open |", "").replace("| VER-23 | Phase 69 | Complete |", ""), self.roadmap)):
            with self.subTest(requirements=requirements[:30]), self.assertRaises(self.module.VerifyError):
                self.report(requirements, roadmap)

    def test_duplicates_on_each_mapping_surface_refuse(self):
        changes = [
            (self.requirements.replace("## Scope Boundaries", "- [ ] **EXP-01**: duplicate\n## Scope Boundaries"), self.roadmap),
            (self.requirements + "| EXP-01 | Phase 65 | Pending |\n", self.roadmap),
            (self.requirements, self.roadmap.replace("**Requirements**: EXP-01", "**Requirements**: EXP-01, EXP-01")),
            (self.requirements, self.roadmap.replace("**Requirements**: VER-23", "**Requirements**: VER-23, EXP-01")),
            (self.requirements, self.roadmap.replace("## Progress", "### Phase 65: Duplicate\n**Requirements**: EXP-01\n## Progress")),
        ]
        for requirements, roadmap in changes:
            with self.subTest(roadmap=roadmap[:50]), self.assertRaises(self.module.VerifyError):
                self.report(requirements, roadmap)

    def test_orphan_extra_conflict_and_multiple_phase_rows_refuse(self):
        changes = [
            (self.requirements.replace("| EXP-01 | Phase 65 | Open |", ""), self.roadmap),
            (self.requirements + "| EXTRA-01 | Phase 65 | Open |\n", self.roadmap),
            (self.requirements, self.roadmap.replace("**Requirements**: EXP-01", "**Requirements**: EXP-01, EXTRA-01")),
            (self.requirements.replace("| EXP-01 | Phase 65", "| EXP-01 | Phase 69"), self.roadmap),
            (self.requirements.replace("| EXP-01 | Phase 65", "| EXP-01 | Phase 65, Phase 69"), self.roadmap),
        ]
        for requirements, roadmap in changes:
            with self.subTest(requirements=requirements[-90:]), self.assertRaises(self.module.VerifyError):
                self.report(requirements, roadmap)

    def test_missing_phase_directory_and_phase_requirement_line_refuse(self):
        self.phases.remove("69")
        with self.assertRaisesRegex(self.module.VerifyError, "missing_phases"):
            self.report()
        self.phases.add("69")
        for roadmap in (self.roadmap.replace("**Requirements**: VER-23", "**Requirements**:"),
                        self.roadmap.replace("**Requirements**: VER-23\n", "")):
            with self.subTest(roadmap=roadmap[-120:]), self.assertRaises(self.module.VerifyError):
                self.report(roadmap=roadmap)

    def test_each_invocation_rereads_live_sources(self):
        m = self.module
        original = Path.read_text
        versions = [self.requirements, self.requirements.replace("**EXP-01**", "**EXP-99**")]

        def read_text(path, *args, **kwargs):
            if path == m.ROOT / ".planning/REQUIREMENTS.md":
                return versions.pop(0)
            if path == m.ROOT / ".planning/ROADMAP.md":
                return self.roadmap
            return original(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", read_text):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(m.main(["traceability"]), 0)
                self.assertEqual(m.main(["traceability"]), 1)

    def test_all_runs_each_check_and_only_emits_success_after_every_pass(self):
        m = self.module
        calls = []
        with mock.patch.object(m, "check_sources", side_effect=lambda: calls.append("sources")):
            with mock.patch.object(m, "check_cost", side_effect=lambda: calls.append("cost")):
                with mock.patch.object(m, "check_traceability", side_effect=lambda: calls.append("traceability")):
                    with contextlib.redirect_stdout(io.StringIO()) as output:
                        self.assertEqual(m.main(["all"]), 0)
        self.assertEqual(calls, ["sources", "cost", "traceability"])
        self.assertIn("PHASE69-ALL-OK", output.getvalue())
        with mock.patch.object(m, "check_sources", side_effect=m.VerifyError("bad source")):
            with contextlib.redirect_stdout(io.StringIO()) as output, contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(m.main(["all"]), 1)
        self.assertNotIn("PHASE69-ALL-OK", output.getvalue())


if __name__ == "__main__":
    unittest.main()
