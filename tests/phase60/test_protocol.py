"""Phase 60 (SPEC Requirement 4): tests for the run protocol builder, writer and loader.

The run protocol pre-registers how every real arm will run and fingerprints the code
and the frozen inputs those arms use. These tests read the real repository (to build a
protocol from the real files) and write only under temporary directories; the real
evidence tree is never touched and no real protocol or preflight is written. A test
that needs a file to change works on a "mirror": byte-identical copies of everything the
protocol reads or pins, placed in a temporary directory (a git repository when the test
needs tracked and clean files), and changes the copy.

The module under test is reached through a helper, so a run against a tree that does
not have it yet fails on the planned behavior instead of at import. Expected values are
written out here from the plan and the gap register, not read back from the module.
"""

from __future__ import annotations

import ast
import atexit
import contextlib
import copy
import functools
import hashlib
import importlib
import io
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from pinn.training.config import OptConfig
from pinn.training.grad_clip import DEFAULT_C_STAGE_TABLE
from pinn.verification import evidence_io
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.learnability_arms import SEQUENCES, TIMING_STEPS, catalog
from pinn.verification.learnability_data import HarnessHalt
from tests.phase59.test_evidence_verifier import commit_all
from tests.phase60.test_g2 import init_quiet_repo

ROOT = Path(__file__).resolve().parents[2]

PHASE59 = ".planning/phases/59-read-only-baseline-scorecard/evidence"
PANELS = f"{PHASE59}/census/panels.json"
PICKS = f"{PHASE59}/survey/picks.json"
TWO_KEPLER = f"{PHASE59}/baselines/two_kepler.json"
METADATA = "runs/stage0-v23g7-seed42/training_metadata.json"
EVIDENCE = ".planning/phases/60-single-system-learnability/evidence"
SUCCESSOR = f"{EVIDENCE}/scorer-successor.json"
PROTOCOL_PATH = f"{EVIDENCE}/run-protocol.json"
PREFLIGHT_PATH = f"{EVIDENCE}/preflight/records.json"
SCORER = "pinn/verification/feasibility_scorer.py"
SCORECARD = "pinn/verification/artifacts/feasibility_scorecard_v1.json"
R_REF = "pinn/verification/artifacts/r_ref_stage0.json"
INPUTS = (PANELS, PICKS, TWO_KEPLER, METADATA, SUCCESSOR)

# PINNED_MODULES as the plan lists it: every module and artifact a real arm executes or reads.
PLAN_PINNED = (
    "pinn/verification/learnability_arms.py",
    "pinn/verification/learnability_data.py",
    "pinn/verification/learnability_losses.py",
    "pinn/verification/learnability_run.py",
    "pinn/verification/learnability_g2.py",
    "pinn/verification/learnability_ruling.py",
    "pinn/verification/learnability_protocol.py",
    "pinn/verification/diagnostic_architecture.py",
    "pinn/verification/gate04_omega_remeasure.py",
    "pinn/verification/gate04_train_free.py",
    "pinn/verification/feasibility_scorer.py",
    "pinn/verification/feasibility_scorecard.py",
    "pinn/verification/production_reference.py",
    "pinn/verification/split_allowlist.py",
    "pinn/verification/evidence_io.py",
    "pinn/loss_catalog.py",
    "pinn/physics_residual.py",
    "pinn/network.py",
    "pinn/architecture_spec.py",
    "pinn/constants.py",
    "pinn/training/controllers.py",
    "pinn/training/config.py",
    "pinn/training/grad_clip.py",
    "pinn/training/scheduled_weights.py",
    "pinn/training/determinism.py",
    "pinn/training/atomic_io.py",
    "pinn/training/signals.py",
    "pinn/data/batches.py",
    "pinn/data/preprocessing.py",
    "pinn/data/types.py",
    SCORECARD,
    R_REF,
    f"{EVIDENCE}/launch_phase60_arm.py",
)

S_H = 22.321729071058996
EPS_H = 0.0022321729071058997
NORMALIZER = "77526e53c394bbac4d4a0e8fdd5a7688f0bda108d41c56277b55ad426a7a79f6"
SCORECARD_SHA = "f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b"
R_REF_VALUE = 19749775821.24417
NO_RESCUE = "no rescue"
GO_TO_VERDICT = "checkpoint ④ answered go to the verdict"
HEX64 = re.compile(r"[0-9a-f]{64}")
HEX40 = re.compile(r"[0-9a-f]{40}")


def protocol_module(case):
    """The module under test, or a test failure that says it is missing."""
    try:
        return importlib.import_module("pinn.verification.learnability_protocol")
    except ModuleNotFoundError as exc:
        if exc.name != "pinn.verification.learnability_protocol":
            raise
        case.fail("pinn.verification.learnability_protocol is missing")


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path):
    return sha256_bytes(Path(path).read_bytes())


def canonical(payload):
    return evidence_io.canonical_json_bytes(payload)


def jsonable(payload):
    """``payload`` as it reads back from a canonical JSON file."""
    return json.loads(canonical(payload))


def write_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def edit_json(root, relative, change):
    """Read a JSON file under ``root``, let ``change`` mutate it, and write it back."""
    path = Path(root) / relative
    payload = json.loads(path.read_text(encoding="utf-8"))
    change(payload)
    write_json(path, payload)


@functools.lru_cache(maxsize=None)
def real_head():
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


_REAL = {}


def real_protocol(case):
    """A protocol built from the real repository at its HEAD (built once per process)."""
    module = protocol_module(case)
    if "protocol" not in _REAL:
        _REAL["protocol"] = module.build_protocol(repo_root=ROOT, amendment_commit=real_head())
    return copy.deepcopy(_REAL["protocol"])


# ---------------------------------------------------------------------------
# Mirrors: copies of everything the protocol reads or pins.
# ---------------------------------------------------------------------------

_HOME = []
_TEMPLATES = {}


def _template_home():
    if not _HOME:
        home = tempfile.TemporaryDirectory(prefix="phase60-protocol-templates-")
        atexit.register(home.cleanup)
        _HOME.append(home)
    return Path(_HOME[0].name).resolve()


def copy_inputs(destination):
    """Copy every pinned module and every input file the protocol reads into ``destination``."""
    for relative in (*PLAN_PINNED, *INPUTS):
        target = Path(destination) / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)


def mirror(case, *, git=False):
    """A private mirror. With ``git`` it is a repository whose HEAD commits the copies.

    Returns ``(root, first_commit)``; ``first_commit`` is ``None`` without ``git``.
    """
    key = "git" if git else "plain"
    template = _TEMPLATES.get(key)
    if template is None:
        path = _template_home() / f"mirror-{key}"
        path.mkdir()
        commit = None
        if git:
            init_quiet_repo(path)
        copy_inputs(path)
        if git:
            commit = commit_all(path, "mirror of the pinned files")
        template = _TEMPLATES[key] = (path, commit)
    tmp = tempfile.TemporaryDirectory(prefix="phase60-protocol-mirror-")
    case.addCleanup(tmp.cleanup)
    root = Path(tmp.name).resolve()
    shutil.copytree(template[0], root, symlinks=True, dirs_exist_ok=True)
    return root, template[1]


def run_cli(module, argv):
    """Run ``module.main`` in this process; return ``(exit code, stdout text)``."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = module.main(argv)
    return code, buffer.getvalue().strip()


# ---------------------------------------------------------------------------
# The module's contract.
# ---------------------------------------------------------------------------

class ModuleContractTests(unittest.TestCase):
    def setUp(self):
        self.P = protocol_module(self)

    def test_the_pinned_list_is_the_plans_list_in_the_plans_order(self):
        self.assertEqual(tuple(self.P.PINNED_MODULES), PLAN_PINNED)
        self.assertEqual(len(set(self.P.PINNED_MODULES)), len(self.P.PINNED_MODULES))

    def test_every_pinned_path_exists_in_the_repository(self):
        for relative in self.P.PINNED_MODULES:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_schemas_and_paths_are_the_plans(self):
        self.assertEqual(self.P.PROTOCOL_SCHEMA, "phase60-run-protocol/v1")
        self.assertEqual(self.P.PREFLIGHT_SCHEMA, "phase60-preflight/v1")
        self.assertEqual(Path(self.P.PROTOCOL_REL).as_posix(), PROTOCOL_PATH)
        self.assertEqual(Path(self.P.PREFLIGHT_REL).as_posix(), PREFLIGHT_PATH)
        self.assertEqual(
            Path(self.P.PROTOCOL_DOC_REL).as_posix(),
            ".planning/phases/60-single-system-learnability/60-RUN-PROTOCOL.md",
        )

    def test_the_planned_names_are_exported(self):
        for name in (
            "PROTOCOL_SCHEMA", "PROTOCOL_REL", "PROTOCOL_DOC_REL", "PREFLIGHT_REL",
            "PINNED_MODULES", "ProtocolDrift", "AdmissionRefused", "build_protocol",
            "write_protocol", "load_protocol", "write_preflight", "admit_arm", "main",
        ):
            with self.subTest(name=name):
                self.assertIn(name, self.P.__all__)
                self.assertTrue(hasattr(self.P, name))

    def test_the_exception_types(self):
        self.assertTrue(issubclass(self.P.ProtocolDrift, RuntimeError))
        self.assertTrue(issubclass(self.P.AdmissionRefused, RuntimeError))
        drift = self.P.ProtocolDrift("a.py differs", paths=["a.py"])
        self.assertEqual(list(drift.paths), ["a.py"])

    def test_the_docstring_carries_the_phase_60_marker(self):
        source = (ROOT / "pinn/verification/learnability_protocol.py").read_text(encoding="utf-8")
        first = (ast.get_docstring(ast.parse(source)) or "").splitlines()[0]
        self.assertEqual(
            first, "Phase 60 (SPEC R4): the run protocol, the record preflight and real-arm admission."
        )

    def test_the_module_does_not_import_the_runner(self):
        source = (ROOT / "pinn/verification/learnability_protocol.py").read_text(encoding="utf-8")
        for node in ast.walk(ast.parse(source)):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""] + [
                    f"{node.module}.{alias.name}" for alias in node.names
                ]
            for name in names:
                with self.subTest(name=name):
                    self.assertFalse(
                        name == "pinn.verification.learnability_run"
                        or name.startswith("pinn.verification.learnability_run."),
                        name,
                    )
                    self.assertNotEqual(name, "learnability_run")


# ---------------------------------------------------------------------------
# The content, built from the real repository.
# ---------------------------------------------------------------------------

class ContentTests(unittest.TestCase):
    def setUp(self):
        self.P = protocol_module(self)
        self.p = real_protocol(self)
        self.card = load_scorecard()

    def section(self, name):
        return jsonable(dict(self.card.section(name)))

    def test_identity_runtime_and_cross_check(self):
        p = self.p
        self.assertEqual(p["schema"], "phase60-run-protocol/v1")
        self.assertEqual(p["seed"], 42)
        self.assertEqual(p["runtime"], {"dtype": "float32", "device": "mps"})
        self.assertEqual(p["cross_check_runtime"], {"dtype": "float64", "device": "cpu"})
        self.assertEqual(p["amendment_commit"], real_head())
        self.assertIsNone(p["preflight_sha256"])
        self.assertIn("not consulted", p["runtime_rule"])
        self.assertIsInstance(p["plain_language"], str)
        self.assertTrue(p["plain_language"].strip())

    def test_the_schedule_is_the_ratified_adam_cosine_with_the_trainers_constants(self):
        s = self.p["schedule"]
        opt = OptConfig()
        self.assertEqual(s["lr_base"], 0.001)
        self.assertEqual(s["lr_decay"], 0.7)
        self.assertEqual(s["betas"], [0.9, 0.999])
        self.assertEqual(s["eps"], 1e-8)
        self.assertEqual(s["data_only_stage"], 0)
        self.assertEqual(s["probe_stages"], {"2279": 4, "3418": 6})
        self.assertEqual(s["warmup"], "min(2000, floor(0.1 B))")
        self.assertEqual(
            s["extension"], "second cosine of length B from LR_k, Adam state kept, no re-ramp"
        )
        self.assertEqual(
            (s["lr_base"], s["lr_decay"], s["betas"], s["eps"]),
            (opt.adam_lr_base, opt.adam_lr_decay, list(opt.adam_betas), opt.adam_eps),
        )
        self.assertEqual(
            s["lr_by_stage"],
            {"0": opt.lr_for_stage(0), "4": opt.lr_for_stage(4), "6": opt.lr_for_stage(6)},
        )
        self.assertEqual(s["source"], "D-01, D-02, D-03, D-04, D-05")

    def test_the_clip_rule_is_gap_60_03(self):
        c = self.p["clip"]
        self.assertEqual(c["source"], "GAP-60-03")
        self.assertEqual(c["table"], {"0": 8.5, "4": 3.0, "6": 3.0})
        self.assertEqual(c["table"], {str(k): DEFAULT_C_STAGE_TABLE[k] for k in (0, 4, 6)})
        self.assertEqual(c["median_floor"], 1e-6)
        self.assertIs(c["adam_only"], True)
        self.assertIs(c["clip_data_only_arms"], True)

    def test_timing_is_gap_60_04_and_cadence_is_the_frozen_fraction(self):
        t = self.p["timing"]
        self.assertEqual(t["source"], "GAP-60-04")
        self.assertEqual((t["data_only_steps"], t["physics_steps"]), (500, 50))
        self.assertEqual(
            (t["data_only_steps"], t["physics_steps"]),
            (TIMING_STEPS["data_only"], TIMING_STEPS["physics"]),
        )
        self.assertIs(t["all_steps_timed"], True)
        self.assertEqual(t["minimum_steps"], self.card.section("budget_rule")["timing_run_min_steps"])
        cadence = self.p["cadence"]
        self.assertEqual(cadence["max_fraction"], 0.05)
        self.assertEqual(
            cadence["max_fraction"],
            self.card.section("budget_rule")["scoring_cadence_max_fraction"],
        )
        self.assertIn("floor(0.05 B)", cadence["rule"])

    def test_the_budget_is_the_frozen_budget_rule(self):
        self.assertEqual(self.p["budget"], self.section("budget_rule"))
        self.assertEqual(self.p["budget"]["cap_hours_single_system"], 3.0)
        self.assertEqual(self.p["budget"]["extensions_max"], 1)

    def test_the_polish_is_the_scorecards_polish_and_gap_60_05(self):
        polish = self.p["polish"]
        for key, value in self.section("lbfgs_polish").items():
            with self.subTest(key=key):
                self.assertEqual(polish[key], value)
        self.assertEqual(polish["lbfgs_max_iter"], 50)
        self.assertEqual(polish["lbfgs_history_size"], 10)
        self.assertEqual(polish["lbfgs_line_search"], "strong_wolfe")
        self.assertEqual(polish["stop_after_outer_calls_without_improvement"], 5)
        self.assertEqual(polish["stop_at_fraction_of_adam_wall_time"], 0.25)
        self.assertEqual(polish["source"], "GAP-60-05")
        for key in ("improvement", "polish_state", "adam_wall", "outer_call", "non_finite",
                    "e_never_steers"):
            with self.subTest(rule=key):
                self.assertIsInstance(polish[key], str)
                self.assertTrue(polish[key].strip())

    def test_divergence_cross_check_and_weights_rules(self):
        d = self.p["divergence"]
        self.assertEqual(d["source"], "GAP-60-06")
        self.assertIs(d["budget_outcome_called"], False)
        self.assertIs(d["restart"], False)
        c = self.p["cross_check"]
        self.assertEqual(c["source"], "GAP-60-07")
        self.assertEqual(c["runtime"], {"dtype": "float64", "device": "cpu"})
        self.assertIs(c["take_the_better"], False)
        self.assertEqual(c["scope"], "both scored states of every real arm")
        w = self.p["weights"]
        self.assertEqual(w["source"], "D-10, GAP-60-08")
        self.assertEqual(w["files"], ["adam.weights", "polish.weights"])
        self.assertIn("weights_only=True", w["load"])
        self.assertIn("plain git", w["git"])

    def test_the_first_completed_run_is_the_result(self):
        f = self.p["first_result"]
        self.assertIn("first completed run is the result", f["rule"])
        self.assertIn("re-scores the committed weights", f["re_derive"])
        self.assertIn("does not retrain", f["re_derive"])
        self.assertIn("One seed", f["seeds"])

    def test_the_g2_family(self):
        g = self.p["g2"]
        self.assertEqual(g["grid"], [60.0, 120.0, 240.0, 480.0])
        self.assertEqual(g["grid"], self.section("gate_g2")["grid"])
        self.assertEqual(g["locked_value"], 30.0)
        self.assertEqual(g["inner_laps"], {"1632": 10.47, "851": 18.61, "4658": 39.35})
        self.assertIsNone(g["failed_confirmation_pre_answer"])
        self.assertEqual(g["other_settings_label"],
                         "reached Tier 1, not confirmed (one-confirmation budget)")
        self.assertEqual(g["sweep_pairs"], [
            {"failing": [1632, 851, 4658], "sweep": 1632, "confirmation": 851, "uncovered": 4658},
            {"failing": [1632, 851], "sweep": 1632, "confirmation": 851, "uncovered": 4658},
            {"failing": [1632, 4658], "sweep": 1632, "confirmation": 4658, "uncovered": 851},
            {"failing": [851, 4658], "sweep": 851, "confirmation": 4658, "uncovered": 1632},
        ])
        for key in ("sweep_rule", "confirmation_rule", "rescue_rule", "failed_confirmation_rule"):
            with self.subTest(rule=key):
                self.assertTrue(g[key].strip())
        self.assertIn("GAP-60-09", g["failed_confirmation_rule"])

    def test_the_skip_reasons_are_the_two_exact_strings(self):
        self.assertEqual(self.p["skip_reasons"], [NO_RESCUE, GO_TO_VERDICT])
        raw = canonical(self.p)
        self.assertIn(b'"checkpoint \\u2463 answered go to the verdict"', raw)
        self.assertIn(b'"no rescue"', raw)

    def test_the_panel_the_probes_and_the_formula_come_from_the_phase_59_files(self):
        self.assertEqual(self.p["panel"]["systems"], [1632, 851, 4658])
        self.assertEqual(self.p["panel"]["inner_laps"], {"1632": 10.47, "851": 18.61, "4658": 39.35})
        self.assertEqual(self.p["panel"]["source"],
                         {"path": PANELS, "sha256": sha256_file(ROOT / PANELS)})
        probes = self.p["probes"]
        self.assertEqual(probes["picks"],
                         {"stage4b": "standard/base/2279", "stage6": "standard/base/3418"})
        self.assertEqual(probes["stages"], {"2279": 4, "3418": 6})
        self.assertEqual(probes["source"], {"path": PICKS, "sha256": sha256_file(ROOT / PICKS)})
        self.assertEqual(probes["formula"], "not applicable: no hierarchical split")
        formula = self.p["formula"]
        self.assertEqual(formula["E_formula"], {
            "1632": 0.916813577071981,
            "851": 0.4312413103776787,
            "4658": 1.9697113677004474,
        })
        self.assertEqual(formula["source"],
                         {"path": TWO_KEPLER, "sha256": sha256_file(ROOT / TWO_KEPLER)})

    def test_s_h_the_normalizer_and_the_governed_reference(self):
        s = self.p["s_h"]
        self.assertEqual((s["value"], s["eps_h"]), (S_H, EPS_H))
        self.assertEqual(s["source_path"], METADATA)
        self.assertEqual(s["source_sha256"], sha256_file(ROOT / METADATA))
        self.assertEqual(s["source"], "GAP-60-12")
        self.assertEqual(self.p["normalizer_stats_sha256"], NORMALIZER)
        r = self.p["r_ref_governed"]
        self.assertEqual(r["value"], R_REF_VALUE)
        self.assertEqual(r["path"], R_REF)
        self.assertEqual(r["sha256"], "c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff")
        self.assertEqual(r["sha256"], sha256_file(ROOT / R_REF))
        rule = self.p["r_ref_rule"]
        self.assertEqual(rule["note"], "Stage-0 reference in force, applied unchanged")
        self.assertEqual(rule["source"], "D-08 with GAP-60-10")
        self.assertIn("context column", rule["rule"])

    def test_the_scorecard_and_scorer_digests_and_the_successor(self):
        successor = json.loads((ROOT / SUCCESSOR).read_text(encoding="utf-8"))
        self.assertEqual(self.p["scorecard_sha256"], SCORECARD_SHA)
        self.assertEqual(self.p["scorecard_sha256"], sha256_file(ROOT / SCORECARD))
        self.assertEqual(self.p["scorer_sha256"], successor["successor_sha256"])
        self.assertEqual(self.p["scorer_sha256"], sha256_file(ROOT / SCORER))
        self.assertEqual(self.p["scorer_successor"]["path"], SCORER)
        self.assertEqual(self.p["scorer_successor"]["predecessor_sha256"],
                         successor["predecessor_sha256"])
        self.assertEqual(self.p["scorer_successor"]["record_sha256"], sha256_file(ROOT / SUCCESSOR))

    def test_module_digests_cover_the_pinned_list_and_equal_the_files(self):
        pins = self.p["module_sha256"]
        self.assertEqual(sorted(pins), sorted(PLAN_PINNED))
        for relative, digest in pins.items():
            with self.subTest(path=relative):
                self.assertEqual(digest, sha256_file(ROOT / relative))
        self.assertEqual(pins, evidence_io.module_hashes(PLAN_PINNED, repo_root=ROOT))

    def test_the_catalog_and_the_sequences_are_pinned_whole(self):
        arms = self.p["catalog"]
        self.assertEqual(len(arms), 42)
        self.assertEqual(sorted(arms), sorted(catalog()))
        row = arms["r1-1632"]
        self.assertEqual(
            (row["rung"], row["path"], row["loss_arm"], row["train_key"], row["score_key"],
             row["beside_key"], row["lr_stage"], row["clip_stage"], row["omega_provenance"],
             row["grid_omega"], row["counted"], row["run_kind"]),
            ("1", "rung1", "data_only", "hierarchical/gold/1632", "hierarchical/gold/1632",
             "hierarchical/base/1632", 0, 0, "locked", None, True, "real"),
        )
        probe = arms["p2b-2279"]
        self.assertEqual((probe["train_key"], probe["lr_stage"], probe["clip_stage"], probe["counted"]),
                         ("standard/base/2279", 4, 4, False))
        sweep = arms["g2s-1632-w060"]
        self.assertEqual((sweep["grid_omega"], sweep["omega_provenance"]), (60.0, "g2_sweep_override"))
        sequences = self.p["sequences"]
        self.assertEqual(len(sequences), 51)
        self.assertEqual({name: list(ids) for name, ids in SEQUENCES.items()}, sequences)

    def test_the_owner_stops_are_the_nine_the_plan_lists(self):
        self.assertEqual(
            [stop["id"] for stop in self.p["owner_stops"]],
            [
                "missing_formula_on_counted_system",
                "rescue",
                "undeterminable_improvement_rate",
                "cross_check_disagreement",
                "failed_confirmation_without_pre_answer",
                "arm_cannot_resume_or_non_governed_exit",
                "blocked_record",
                "gate04_block_on_continue",
                "protocol_drift_after_real_record",
            ],
        )
        for stop in self.p["owner_stops"]:
            with self.subTest(stop=stop["id"]):
                self.assertTrue(stop["when"].strip())
                self.assertTrue(stop["source"].strip())

    def test_the_readout_notes_name_d_04_d_05_d_08_and_the_one_seed_limit(self):
        notes = self.p["readout_notes"]
        self.assertTrue(any(
            note.startswith("D-04:") and "low-rate tail" in note for note in notes
        ), notes)
        self.assertTrue(any(
            note.startswith("D-05:") and "starts from scratch" in note
            and "0.7 factor assumes weights carried forward" in note
            for note in notes
        ), notes)
        self.assertTrue(any(
            note.startswith("D-08") and "Stage-0 reference in force, applied unchanged" in note
            for note in notes
        ), notes)
        self.assertTrue(any("One seed per arm" in note and "limit for the verdict" in note
                            for note in notes), notes)

    def test_the_decisions_and_the_approved_setting_rule(self):
        decisions = self.p["decisions"]
        self.assertEqual(sorted(decisions), ["D-06", "D-07", "D-08", "D-09", "D-10", "D-11"])
        self.assertIn("never halts", decisions["D-06"])
        self.assertIn("GATE-04", decisions["D-07"])
        self.assertIn("committed ruling", decisions["D-11"])
        rule = self.p["approved_omega_rule"]
        self.assertEqual(rule["source"], "GAP-60-11 and D-11")
        self.assertEqual(rule["ruling_file"],
                         ".planning/phases/60-single-system-learnability/60-CHECKPOINT-4-RULING.md")
        self.assertIn("on_grid", rule["rule"])
        self.assertIn("equals_confirmed", rule["rule"])

    def test_the_protocol_is_plain_json_and_names_no_absolute_path(self):
        self.assertEqual(self.p, jsonable(self.p))
        text = canonical(self.p).decode("ascii")
        self.assertNotIn(str(Path.home()), text)
        self.assertNotIn(str(ROOT), text)
        self.assertEqual(HEX40.fullmatch(self.p["amendment_commit"]) is not None, True)
        for relative in self.p["module_sha256"]:
            self.assertFalse(relative.startswith("/"), relative)


# ---------------------------------------------------------------------------
# The inputs build_protocol pins.
# ---------------------------------------------------------------------------

class PinCheckTests(unittest.TestCase):
    def setUp(self):
        self.P = protocol_module(self)
        self.root, _commit = mirror(self)

    def build(self, **options):
        options.setdefault("amendment_commit", real_head())
        return self.P.build_protocol(repo_root=self.root, **options)

    def assertDrift(self, relative, **options):
        with self.assertRaises(self.P.ProtocolDrift) as caught:
            self.build(**options)
        self.assertIn(relative, list(caught.exception.paths))
        return caught.exception

    def test_a_mirror_builds_the_same_protocol_as_the_real_repository(self):
        self.assertEqual(self.build(), real_protocol(self))

    def test_a_panel_other_than_the_pinned_three_is_refused(self):
        def other_id(payload):
            payload["singles"][0]["id"] = 1633

        def swapped(payload):
            payload["singles"][0], payload["singles"][1] = payload["singles"][1], payload["singles"][0]

        def dropped(payload):
            payload["singles"].pop()

        for label, change in (("other id", other_id), ("swapped", swapped), ("dropped", dropped)):
            with self.subTest(case=label):
                root, _ = mirror(self)
                edit_json(root, PANELS, change)
                with self.assertRaises(self.P.ProtocolDrift) as caught:
                    self.P.build_protocol(repo_root=root, amendment_commit=real_head())
                self.assertIn(PANELS, list(caught.exception.paths))

    def test_a_lap_count_that_rounds_differently_is_refused(self):
        for index, value in ((0, 10.48), (1, 18.62), (2, 39.34)):
            with self.subTest(index=index, value=value):
                root, _ = mirror(self)
                edit_json(root, PANELS, lambda payload: payload["singles"][index].update(N_in=value))
                with self.assertRaises(self.P.ProtocolDrift) as caught:
                    self.P.build_protocol(repo_root=root, amendment_commit=real_head())
                self.assertIn(PANELS, list(caught.exception.paths))

    def test_a_probe_pick_other_than_2279_and_3418_is_refused(self):
        for stage, record in (("stage4b", "standard/base/1916"), ("stage6", "standard/base/512")):
            with self.subTest(stage=stage):
                root, _ = mirror(self)
                edit_json(root, PICKS, lambda payload: payload[stage].update(record=record))
                with self.assertRaises(self.P.ProtocolDrift) as caught:
                    self.P.build_protocol(repo_root=root, amendment_commit=real_head())
                self.assertIn(PICKS, list(caught.exception.paths))

    def test_an_s_h_value_other_than_the_gap_60_12_value_is_refused(self):
        for key, value in (("s_h", 22.4), ("eps_h", 0.0023), ("s_h", None)):
            with self.subTest(key=key, value=value):
                root, _ = mirror(self)
                edit_json(root, METADATA, lambda payload: payload.update({key: value}))
                with self.assertRaises(self.P.ProtocolDrift) as caught:
                    self.P.build_protocol(repo_root=root, amendment_commit=real_head())
                self.assertIn(METADATA, list(caught.exception.paths))

    def test_a_scorer_other_than_the_successor_is_refused(self):
        scorer = self.root / SCORER
        scorer.write_bytes(scorer.read_bytes() + b"\n# changed\n")
        self.assertDrift(SCORER)

    def test_a_successor_record_that_disagrees_with_the_scorer_or_itself_is_refused(self):
        for label, change, named in (
            ("another digest", lambda payload: payload.update(successor_sha256="0" * 64), SCORER),
            ("another path", lambda payload: payload.update(path="pinn/verification/evidence_io.py"), SUCCESSOR),
            ("a missing digest", lambda payload: payload.pop("successor_sha256"), SUCCESSOR),
            ("a malformed digest", lambda payload: payload.update(successor_sha256="XYZ"), SUCCESSOR),
        ):
            with self.subTest(case=label):
                root, _ = mirror(self)
                edit_json(root, SUCCESSOR, change)
                with self.assertRaises(self.P.ProtocolDrift) as caught:
                    self.P.build_protocol(repo_root=root, amendment_commit=real_head())
                self.assertIn(named, list(caught.exception.paths))

    def test_a_scorecard_that_is_not_the_frozen_file_is_refused(self):
        path = self.root / SCORECARD
        path.write_bytes(path.read_bytes() + b" ")
        self.assertDrift(SCORECARD)

    def test_a_formula_row_that_is_not_applicable_is_refused(self):
        def not_applicable(payload):
            payload["rows"]["singles"][0]["applicable"] = False

        edit_json(self.root, TWO_KEPLER, not_applicable)
        self.assertDrift(TWO_KEPLER)

    def test_a_governed_reference_that_does_not_load_is_refused(self):
        edit_json(self.root, R_REF, lambda payload: payload.update(valid=False))
        self.assertDrift(R_REF)

    def test_an_amendment_commit_that_is_not_a_full_lowercase_hash_is_refused(self):
        for value in ("", "abc", "A" * 40, "g" * 40, "a" * 39, "a" * 41, None, 7):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.build(amendment_commit=value)

    def test_a_preflight_digest_must_be_a_sha256_or_none(self):
        self.assertEqual(self.build(preflight_sha256="ab" * 32)["preflight_sha256"], "ab" * 32)
        for value in ("ab" * 31, "AB" * 32, "zz" * 32, 5):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.build(preflight_sha256=value)


# ---------------------------------------------------------------------------
# Veto and pre-answer.
# ---------------------------------------------------------------------------

class VetoTests(unittest.TestCase):
    def setUp(self):
        self.P = protocol_module(self)

    def build(self, **options):
        return self.P.build_protocol(repo_root=ROOT, amendment_commit=real_head(), **options)

    def test_the_defaults_keep_clipping_and_leave_the_confirmation_open(self):
        p = self.build()
        self.assertIs(p["clip"]["clip_data_only_arms"], True)
        self.assertIsNone(p["g2"]["failed_confirmation_pre_answer"])

    def test_a_clipping_veto_is_recorded_and_changes_nothing_else(self):
        vetoed = self.build(clip_data_only_arms=False)
        self.assertIs(vetoed["clip"]["clip_data_only_arms"], False)
        expected = real_protocol(self)
        expected["clip"]["clip_data_only_arms"] = False
        self.assertEqual(vetoed, expected)

    def test_a_pre_answer_is_recorded_for_no_rescue_and_for_rescue(self):
        for answer in ("no_rescue", "rescue"):
            with self.subTest(answer=answer):
                p = self.build(failed_confirmation_pre_answer=answer)
                self.assertEqual(p["g2"]["failed_confirmation_pre_answer"], answer)

    def test_any_other_pre_answer_is_refused(self):
        for answer in ("", "ask", "No_Rescue", "RESCUE", "none", "null", True, False, 0, 1, [], {}):
            with self.subTest(answer=answer):
                with self.assertRaises(ValueError):
                    self.build(failed_confirmation_pre_answer=answer)

    def test_the_clipping_flag_must_be_a_boolean(self):
        for value in ("no", 0, 1, None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.build(clip_data_only_arms=value)


# ---------------------------------------------------------------------------
# Writing and loading.
# ---------------------------------------------------------------------------

class RoundTripTests(unittest.TestCase):
    def setUp(self):
        self.P = protocol_module(self)
        tmp = tempfile.TemporaryDirectory(prefix="phase60-protocol-evidence-")
        self.addCleanup(tmp.cleanup)
        self.evidence = Path(tmp.name).resolve() / "evidence"

    def write(self):
        protocol = real_protocol(self)
        digest = self.P.write_protocol(protocol, evidence_root=self.evidence)
        return protocol, digest

    def test_the_file_is_the_canonical_json_and_the_returned_digest_is_its_hash(self):
        protocol, digest = self.write()
        path = self.evidence / "run-protocol.json"
        self.assertEqual(path.read_bytes(), canonical(protocol))
        self.assertEqual(digest, sha256_file(path))

    def test_load_returns_the_same_protocol_and_the_files_hash(self):
        protocol, digest = self.write()
        loaded = self.P.load_protocol(
            repo_root=ROOT, evidence_root=self.evidence, require_committed=False
        )
        self.assertEqual(loaded.payload, protocol)
        self.assertEqual(loaded.sha256, digest)
        self.assertEqual(loaded.sha256, sha256_file(self.evidence / "run-protocol.json"))

    def test_the_written_file_names_no_home_directory(self):
        self.write()
        text = (self.evidence / "run-protocol.json").read_text(encoding="ascii")
        self.assertNotIn(str(Path.home()), text)

    def test_a_protocol_outside_git_is_not_a_committed_protocol(self):
        self.write()
        with self.assertRaises(self.P.ProtocolDrift):
            self.P.load_protocol(repo_root=ROOT, evidence_root=self.evidence)

    def test_writing_twice_with_no_record_is_allowed(self):
        _protocol, first = self.write()
        second = self.P.write_protocol(real_protocol(self), evidence_root=self.evidence)
        self.assertEqual(first, second)

    def test_a_record_or_an_owner_stop_blocks_the_write(self):
        for name in ("record.json", "owner-stop.json"):
            with self.subTest(file=name):
                evidence = self.evidence.parent / f"evidence-{name}"
                arm = evidence / "arms" / "r1-1632"
                arm.mkdir(parents=True)
                (arm / name).write_text("{}\n", encoding="utf-8")
                with self.assertRaises(HarnessHalt):
                    self.P.write_protocol(real_protocol(self), evidence_root=evidence)
                self.assertFalse((evidence / "run-protocol.json").exists())

    def test_other_files_under_arms_do_not_block_the_write(self):
        arm = self.evidence / "arms" / "r1-1632"
        arm.mkdir(parents=True)
        (arm / "adam.weights").write_bytes(b"x")
        (self.evidence / "arms" / "README.txt").write_text("note\n", encoding="utf-8")
        self.P.write_protocol(real_protocol(self), evidence_root=self.evidence)
        self.assertTrue((self.evidence / "run-protocol.json").is_file())


class DriftTests(unittest.TestCase):
    def setUp(self):
        self.P = protocol_module(self)
        self.root, self.first = mirror(self, git=True)
        self.evidence = self.root / EVIDENCE
        self.protocol = self.P.build_protocol(repo_root=self.root, amendment_commit=self.first)
        self.digest = self.P.write_protocol(self.protocol, evidence_root=self.evidence)
        commit_all(self.root, "run protocol")

    def load(self, **options):
        options.setdefault("repo_root", self.root)
        options.setdefault("evidence_root", self.evidence)
        return self.P.load_protocol(**options)

    def test_an_unchanged_committed_protocol_loads(self):
        loaded = self.load()
        self.assertEqual(loaded.payload, self.protocol)
        self.assertEqual(loaded.sha256, self.digest)
        self.assertEqual(loaded.path, PROTOCOL_PATH)

    def test_the_default_evidence_root_is_the_repositorys(self):
        loaded = self.P.load_protocol(repo_root=self.root)
        self.assertEqual(loaded.sha256, self.digest)

    def test_each_pinned_file_changed_is_named(self):
        for relative in PLAN_PINNED:
            with self.subTest(path=relative):
                path = self.root / relative
                original = path.read_bytes()
                try:
                    path.write_bytes(original + b"\n")
                    with self.assertRaises(self.P.ProtocolDrift) as caught:
                        self.load()
                    self.assertEqual(list(caught.exception.paths), [relative])
                    self.assertIn(relative, str(caught.exception))
                finally:
                    path.write_bytes(original)
        self.load()

    def test_several_changed_files_are_all_named(self):
        changed = [PLAN_PINNED[0], PLAN_PINNED[10], PLAN_PINNED[31]]
        originals = {relative: (self.root / relative).read_bytes() for relative in changed}
        try:
            for relative in changed:
                (self.root / relative).write_bytes(originals[relative] + b"\n")
            with self.assertRaises(self.P.ProtocolDrift) as caught:
                self.load()
            self.assertEqual(sorted(caught.exception.paths), sorted(changed))
        finally:
            for relative, raw in originals.items():
                (self.root / relative).write_bytes(raw)

    def test_a_missing_pinned_file_is_named(self):
        target = self.root / PLAN_PINNED[3]
        raw = target.read_bytes()
        target.unlink()
        try:
            with self.assertRaises(self.P.ProtocolDrift) as caught:
                self.load()
            self.assertEqual(list(caught.exception.paths), [PLAN_PINNED[3]])
        finally:
            target.write_bytes(raw)

    def rewrite(self, change):
        path = self.evidence / "run-protocol.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        change(payload)
        write_json(path, payload)
        commit_all(self.root, "edit the protocol")

    def test_a_protocol_that_pins_a_different_set_of_files_is_refused(self):
        self.rewrite(lambda payload: payload["module_sha256"].pop(PLAN_PINNED[5]))
        with self.assertRaises(self.P.ProtocolDrift) as caught:
            self.load()
        self.assertIn(PLAN_PINNED[5], list(caught.exception.paths))

    def test_a_protocol_that_pins_an_extra_file_is_refused(self):
        self.rewrite(lambda payload: payload["module_sha256"].update({"pinn/extra.py": "0" * 64}))
        with self.assertRaises(self.P.ProtocolDrift) as caught:
            self.load()
        self.assertIn("pinn/extra.py", list(caught.exception.paths))

    def test_a_wrong_schema_or_a_non_object_is_refused(self):
        self.rewrite(lambda payload: payload.update(schema="phase60-run-protocol/v0"))
        with self.assertRaises(self.P.ProtocolDrift):
            self.load()
        (self.evidence / "run-protocol.json").write_text("[1, 2]\n", encoding="utf-8")
        commit_all(self.root, "not an object")
        with self.assertRaises(self.P.ProtocolDrift):
            self.load()
        (self.evidence / "run-protocol.json").write_text("{not json", encoding="utf-8")
        commit_all(self.root, "not json")
        with self.assertRaises(self.P.ProtocolDrift):
            self.load()

    def test_a_missing_protocol_is_refused(self):
        (self.evidence / "run-protocol.json").unlink()
        with self.assertRaises(self.P.ProtocolDrift):
            self.load(require_committed=False)

    def test_a_dirty_or_untracked_protocol_is_not_a_committed_protocol(self):
        path = self.evidence / "run-protocol.json"
        original = path.read_bytes()
        path.write_bytes(original + b" ")
        with self.assertRaises(self.P.ProtocolDrift) as caught:
            self.load()
        self.assertEqual(list(caught.exception.paths), [PROTOCOL_PATH])
        self.load(require_committed=False)
        path.write_bytes(original)
        self.load()
        subprocess.run(["git", "rm", "--cached", "-q", PROTOCOL_PATH], cwd=self.root, check=True)
        with self.assertRaises(self.P.ProtocolDrift) as caught:
            self.load()
        self.assertEqual(list(caught.exception.paths), [PROTOCOL_PATH])
        self.load(require_committed=False)


# ---------------------------------------------------------------------------
# The command line: write and check.
# ---------------------------------------------------------------------------

class CommandLineTests(unittest.TestCase):
    def setUp(self):
        self.P = protocol_module(self)
        self.root, self.first = mirror(self, git=True)
        self.evidence = self.root / EVIDENCE
        write_json(self.root / PREFLIGHT_PATH, {"schema": "phase60-preflight/v1"})
        commit_all(self.root, "a stand-in preflight")

    def cli(self, *argv):
        return run_cli(self.P, [*argv, "--evidence-root", str(self.evidence)])

    def written(self):
        return json.loads((self.evidence / "run-protocol.json").read_text(encoding="utf-8"))

    def test_write_then_commit_then_check(self):
        code, out = self.cli("write", "--amendment-commit", self.first)
        self.assertEqual(code, 0, out)
        self.assertTrue(out.startswith(f"PROTOCOL-WRITTEN: {PROTOCOL_PATH} sha256 "), out)
        protocol = self.written()
        self.assertEqual(protocol["amendment_commit"], self.first)
        self.assertEqual(protocol["preflight_sha256"], sha256_file(self.root / PREFLIGHT_PATH))
        self.assertIs(protocol["clip"]["clip_data_only_arms"], True)
        self.assertIsNone(protocol["g2"]["failed_confirmation_pre_answer"])
        code, out = self.cli("check")
        self.assertEqual(code, 2, out)
        self.assertTrue(out.startswith("PROTOCOL-DRIFT:"), out)
        commit_all(self.root, "run protocol")
        code, out = self.cli("check")
        self.assertEqual(code, 0, out)
        self.assertEqual(out, f"PROTOCOL-OK: {PROTOCOL_PATH} sha256 {sha256_file(self.evidence / 'run-protocol.json')}")

    def test_the_owner_flags_reach_the_protocol_and_nothing_else_does(self):
        code, out = self.cli(
            "write", "--amendment-commit", self.first,
            "--no-clip-data-only-arms", "--failed-confirmation-pre-answer", "no_rescue",
        )
        self.assertEqual(code, 0, out)
        protocol = self.written()
        self.assertIs(protocol["clip"]["clip_data_only_arms"], False)
        self.assertEqual(protocol["g2"]["failed_confirmation_pre_answer"], "no_rescue")
        code, out = self.cli("write", "--amendment-commit", self.first,
                             "--failed-confirmation-pre-answer", "rescue")
        self.assertEqual(code, 0, out)
        protocol = self.written()
        self.assertIs(protocol["clip"]["clip_data_only_arms"], True)
        self.assertEqual(protocol["g2"]["failed_confirmation_pre_answer"], "rescue")

    def test_an_unknown_pre_answer_is_an_argument_error(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as caught:
            self.cli("write", "--amendment-commit", self.first,
                     "--failed-confirmation-pre-answer", "ask")
        self.assertEqual(caught.exception.code, 2)
        self.assertFalse((self.evidence / "run-protocol.json").exists())

    def test_write_refuses_without_a_preflight(self):
        (self.root / PREFLIGHT_PATH).unlink()
        code, out = self.cli("write", "--amendment-commit", self.first)
        self.assertEqual(code, 2, out)
        self.assertTrue(out.startswith("PROTOCOL-REFUSED:"), out)
        self.assertIn("preflight", out)
        self.assertFalse((self.evidence / "run-protocol.json").exists())

    def test_write_refuses_a_preflight_with_another_schema(self):
        write_json(self.root / PREFLIGHT_PATH, {"schema": "something-else/v1"})
        code, out = self.cli("write", "--amendment-commit", self.first)
        self.assertEqual(code, 2, out)
        self.assertTrue(out.startswith("PROTOCOL-REFUSED:"), out)

    def test_write_refuses_an_amendment_commit_that_is_not_an_ancestor_of_head(self):
        dangling = subprocess.run(
            ["git", "commit-tree", "HEAD^{tree}", "-m", "not in the history"],
            cwd=self.root, capture_output=True, text=True, check=True,
        ).stdout.strip()
        for value in (dangling, "0" * 40, "abc", "not a commit"):
            with self.subTest(commit=value):
                code, out = self.cli("write", "--amendment-commit", value)
                self.assertEqual(code, 2, out)
                self.assertTrue(out.startswith("PROTOCOL-REFUSED:"), out)
                self.assertFalse((self.evidence / "run-protocol.json").exists())

    def test_write_refuses_after_a_real_record(self):
        arm = self.evidence / "arms" / "r1-1632"
        arm.mkdir(parents=True)
        (arm / "record.json").write_text("{}\n", encoding="utf-8")
        code, out = self.cli("write", "--amendment-commit", self.first)
        self.assertEqual(code, 2, out)
        self.assertTrue(out.startswith("PROTOCOL-REFUSED:"), out)
        self.assertFalse((self.evidence / "run-protocol.json").exists())

    def test_write_reports_an_input_that_does_not_match_its_pin_as_drift(self):
        edit_json(self.root, METADATA, lambda payload: payload.update(s_h=22.4))
        code, out = self.cli("write", "--amendment-commit", self.first)
        self.assertEqual(code, 2, out)
        self.assertTrue(out.startswith("PROTOCOL-DRIFT:"), out)
        self.assertIn(METADATA, out)

    def test_check_names_the_changed_file(self):
        self.assertEqual(self.cli("write", "--amendment-commit", self.first)[0], 0)
        commit_all(self.root, "run protocol")
        path = self.root / PLAN_PINNED[13]
        path.write_bytes(path.read_bytes() + b"\n")
        code, out = self.cli("check")
        self.assertEqual(code, 2, out)
        self.assertTrue(out.startswith("PROTOCOL-DRIFT:"), out)
        self.assertIn(PLAN_PINNED[13], out)

    def test_check_with_no_protocol_is_not_ok(self):
        code, out = self.cli("check")
        self.assertEqual(code, 2, out)
        self.assertTrue(out.startswith("PROTOCOL-DRIFT:"), out)


if __name__ == "__main__":
    unittest.main()
