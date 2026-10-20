"""Phase 60 (SPEC Requirements 4 and 8): tests for the record preflight and real-arm admission.

The preflight checks every assigned data file before the first arm and substitutes
nothing for a missing, empty or unreadable record. Admission lets a real arm start only
when the run protocol is drift-free, its records are cleared in the committed preflight,
the amendment commit is in the history, no result exists for it, and the branch the
committed G2 records have taken allows it.

Every admission test builds a synthetic git repository under a temporary directory: byte
identical copies of everything the protocol pins, a preflight written by the real writer
(with the reader replaced by a fake that reports the expected window counts), a run
protocol built by the real builder, and then the G2 records of the scenario. Nothing here
opens the real data root, and nothing is written to the real evidence tree.

The module under test is reached through a helper, so a run against a tree that does not
have these functions yet fails on the planned behavior instead of at import.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import subprocess
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from pinn.data.adapter import EvidenceRedactionError
from pinn.data.types import RecordKey
from pinn.verification import evidence_io
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.learnability_arms import FirstResultExists, catalog
from pinn.verification.learnability_data import HarnessHalt, fixture_context
from tests.phase59.test_evidence_verifier import commit_all
from tests.phase60._fixtures import gold_corpus_fixture
from tests.phase60.test_g2 import ONE_AT_120, ZERO_GRID, Tree, remeasure_payload
from tests.phase60.test_protocol import (
    EVIDENCE,
    METADATA,
    PLAN_PINNED,
    PREFLIGHT_PATH,
    PROTOCOL_PATH,
    R_REF,
    ROOT,
    S_H,
    EPS_H,
    R_REF_VALUE,
    copy_inputs,
    edit_json,
    protocol_module,
    sha256_file,
    write_json,
)

NO_RESCUE = "no rescue"
GOVERNED_SHA = "c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff"
REFERENCE_NOTE = "Stage-0 reference in force, applied unchanged"
APPROVED_PATH = f"{EVIDENCE}/continue/r-ref-approved.json"
RULING_PATH = ".planning/phases/60-single-system-learnability/60-CHECKPOINT-4-RULING.md"
SYNTHETIC_DATA_ROOT = "/phase60/synthetic-data-root"

# The ten assigned records (60-RESEARCH Finding G) and their window counts within T.
TEN_KEYS = (
    "hierarchical/base/1632", "hierarchical/gold/1632",
    "hierarchical/base/851", "hierarchical/gold/851",
    "hierarchical/base/4658", "hierarchical/gold/4658",
    "standard/base/2279", "standard/gold/2279",
    "standard/base/3418", "standard/gold/3418",
)
EXPECTED_WITHIN_T = {
    "hierarchical/gold": 1001, "hierarchical/base": 126,
    "standard/gold": 1001, "standard/base": 59,
}

R1 = {"r1-1632", "r1-851", "r1-4658"}
G2S_1632 = {f"g2s-1632-w{setting:03d}" for setting in (60, 120, 240, 480)}
LADDER = {
    "r2a-1632", "r2a-851", "r2a-4658", "r2b-1632", "r2b-851", "r2b-4658",
    "p1-2279", "p1-3418", "p2b-2279", "p2b-3418",
}
CONTINUE_LADDER = {f"c-{arm}" for arm in LADDER}
ALL_ARMS = tuple(catalog())


def admission_module(case):
    """The module under test, or a test failure that names what is missing."""
    module = protocol_module(case)
    for name in ("write_preflight", "admit_arm", "preflight_records", "open_real_context",
                 "EXPECTED_WITHIN_T"):
        if not hasattr(module, name):
            case.fail(f"pinn.verification.learnability_protocol.{name} is missing")
    return module


# ---------------------------------------------------------------------------
# Fakes for the reader side of the preflight.
# ---------------------------------------------------------------------------

def ok_entry(label):
    variant, fidelity, _identifier = label.split("/")
    within = EXPECTED_WITHIN_T[f"{variant}/{fidelity}"]
    return {
        "status": "ok",
        "split": "train",
        "n_snapshots": within + (1 if fidelity == "gold" else 0),
        "n_within_t": within,
        "dt_out_measured": 0.01,
        "windowed_sha256": hashlib.sha256(label.encode()).hexdigest(),
        "inner_pair": [1, 2],
    }


def fake_preflight(blocked=(), status="missing", wrong_counts=()):
    """A stand-in for ``preflight_records`` that reports the expected counts."""

    def fake(keys, context, *, scorecard):
        report = {}
        for key in keys:
            label = evidence_io.record_key_str(key)
            if label in blocked:
                report[label] = {"status": status, "split": "train"}
            else:
                entry = ok_entry(label)
                if label in wrong_counts:
                    entry["n_within_t"] -= 1
                report[label] = entry
        return report

    return fake


class StubAttestation:
    def __init__(self, **overrides):
        self.overrides = overrides

    def summary(self):
        summary = {
            "schema": "phase59-files-opened/v1",
            "data_root_source": "synthetic",
            "opened": {"train": 10, "validation": 0, "other_under_root": 0},
            "test_split_opened": 0,
            "blocked_attempts": 0,
            "refused_before_open": 0,
        }
        summary.update(self.overrides)
        return summary


def stub_context(**overrides):
    return SimpleNamespace(
        attestation=StubAttestation(**overrides),
        reader=SimpleNamespace(data_root=Path(SYNTHETIC_DATA_ROOT)),
        data_root_source="synthetic",
    )


# ---------------------------------------------------------------------------
# Synthetic repositories with a registered protocol.
# ---------------------------------------------------------------------------

PREFLIGHT_TWEAKS = {
    "counters": lambda payload: payload["attestation"].update(test_split_opened=1),
}
PROTOCOL_TWEAKS = {
    "scorer": lambda payload: payload.update(scorer_sha256="0" * 64),
    "scorecard": lambda payload: payload.update(scorecard_sha256="0" * 64),
}


class RegisteredTree(Tree):
    """A ``Tree`` that can register the pinned files, the preflight and the run protocol."""

    def register(self, *, blocked=(), blocked_status="missing", wrong_counts=(), clip=True,
                 pre_answer=None, amendment=None, preflight_tweak=None, protocol_tweak=None):
        module = admission_module(self.test)
        copy_inputs(self.root)
        first = self.commit("pinned files and Phase 59 inputs")
        if amendment == "dangling":
            first = subprocess.run(
                ["git", "commit-tree", "HEAD^{tree}", "-m", "not in the history"],
                cwd=self.root, capture_output=True, text=True, check=True,
            ).stdout.strip()
        with mock.patch.object(
            module, "preflight_records", fake_preflight(blocked, blocked_status, wrong_counts)
        ):
            module.write_preflight(
                repo_root=self.root, evidence_root=self.evidence, context=stub_context()
            )
        if preflight_tweak:
            edit_json(self.root, PREFLIGHT_PATH, PREFLIGHT_TWEAKS[preflight_tweak])
        self.commit("preflight")
        protocol = module.build_protocol(
            repo_root=self.root,
            amendment_commit=first,
            clip_data_only_arms=clip,
            failed_confirmation_pre_answer=pre_answer,
            preflight_sha256=sha256_file(self.root / PREFLIGHT_PATH),
        )
        module.write_protocol(protocol, evidence_root=self.evidence)
        if protocol_tweak:
            edit_json(self.root, PROTOCOL_PATH, PROTOCOL_TWEAKS[protocol_tweak])
        self.commit("run protocol")
        return first

    def admit(self, arm_id, **options):
        module = admission_module(self.test)
        return module.admit_arm(
            arm_id, repo_root=self.root, evidence_root=self.evidence, **options
        )

    def refusal(self, arm_id, *fragments, **options):
        module = admission_module(self.test)
        with self.test.assertRaises(module.AdmissionRefused) as caught:
            self.admit(arm_id, **options)
        message = str(caught.exception)
        self.test.assertNotIn("\n", message)
        for fragment in fragments:
            self.test.assertIn(fragment, message)
        return message

    def admitted(self):
        """Which of the 42 catalog arms are admitted now."""
        module = admission_module(self.test)
        found = set()
        for arm_id in ALL_ARMS:
            try:
                self.admit(arm_id)
            except module.AdmissionRefused:
                continue
            found.add(arm_id)
        return found

    def with_approved_reference(self, omega, *, verdict="PASS", factor=0.5):
        """A valid re-measured reference (not the governed value) and the record that cites it."""
        governed = json.loads((ROOT / R_REF).read_text(encoding="utf-8"))
        rows = [[value * factor for value in row] for row in governed["raw_bin_means"]]
        ordered = sorted(value for row in rows for value in row)
        governed["raw_bin_means"] = rows
        governed["r_ref"] = (ordered[47] + ordered[48]) / 2.0
        payload = remeasure_payload(
            verdict=verdict, first_omega_0=omega, ruling_sha256=self.ruling_sha()
        )
        if verdict == "PASS":
            artifact = self.path("continue/r-ref-approved.json")
            write_json(artifact, governed)
            payload["r_ref_artifact"] = {"path": APPROVED_PATH, "sha256": sha256_file(artifact)}
        self.write_json(self.path("continue/gate04-remeasure.json"), payload)
        self.commit("re-measure")
        return governed["r_ref"]


def registered(test, name, build=None, **options):
    """A private copy of a registered repository after ``build`` (built once per process)."""

    def make(tree):
        tree.register(**options)
        if build is not None:
            build(tree)

    key = ("admission", name, tuple(sorted(options.items())))
    return RegisteredTree.scenario(test, key, make)


def build_fired(tree, tiers=(0, 0, 0)):
    tree.with_outcome(tiers)


def build_curve(tree, tiers=(0, 0, 0), grid=ONE_AT_120):
    tree.with_outcome(tiers)
    tree.with_curve(grid)


def build_rescue(tree, tiers=(0, 0, 0)):
    """A confirmed rescue: the confirmation record is written and ``rescue`` has run."""
    build_curve(tree, tiers)
    tree.with_confirmation(1)
    code, out = tree.cli("rescue")
    assert code == 3, out
    tree.commit("rescue")


def build_continue(value="120", omega=120.0, verdict="PASS"):
    def build(tree):
        build_rescue(tree)
        tree.with_checkpoint4("continue", value)
        tree.with_approved_reference(omega, verdict=verdict)

    return build


def build_stop(tree):
    build_curve(tree, (0, 0, 0), ZERO_GRID)
    code, out = tree.cli("skip", "--reason", NO_RESCUE)
    assert code == 0, out
    tree.commit("skip records")


# ---------------------------------------------------------------------------
# The contract.
# ---------------------------------------------------------------------------

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.P = admission_module(self)

    def test_the_planned_names_are_exported(self):
        for name in ("write_preflight", "admit_arm", "PREFLIGHT_SCHEMA", "PREFLIGHT_REL"):
            with self.subTest(name=name):
                self.assertIn(name, self.P.__all__)
                self.assertTrue(hasattr(self.P, name))

    def test_the_expected_window_counts_are_the_plans_and_follow_the_grids(self):
        expected = dict(self.P.EXPECTED_WITHIN_T)
        self.assertEqual(expected, EXPECTED_WITHIN_T)
        card = load_scorecard()
        t_max = card.section("scoring_grid")["t_max"]
        # The output steps: gold 0.01 and hierarchical base 0.08 (scorecard), standard base
        # 0.17 (SPEC background). Samples within T are floor(T / dt) + 1.
        steps = {
            "hierarchical/gold": card.section("scoring_grid")["gold_dt"],
            "standard/gold": card.section("scoring_grid")["gold_dt"],
            "hierarchical/base": card.section("scoring_grid")["base_dt"],
            "standard/base": 0.17,
        }
        for name, dt in steps.items():
            with self.subTest(name=name):
                self.assertEqual(int(t_max / dt + 1e-9) + 1, expected[name])


# ---------------------------------------------------------------------------
# The preflight writer.
# ---------------------------------------------------------------------------

class PreflightWriterTests(unittest.TestCase):
    def setUp(self):
        self.P = admission_module(self)
        tmp = tempfile.TemporaryDirectory(prefix="phase60-preflight-evidence-")
        self.addCleanup(tmp.cleanup)
        self.evidence = Path(tmp.name).resolve() / "evidence"
        self.path = self.evidence / "preflight" / "records.json"
        closed = mock.patch.object(
            self.P, "open_real_context", side_effect=AssertionError("the real corpus was opened")
        )
        closed.start()
        self.addCleanup(closed.stop)

    def write(self, *, blocked=(), status="missing", wrong_counts=(), context=None, **options):
        context = stub_context() if context is None else context
        with mock.patch.object(
            self.P, "preflight_records", fake_preflight(blocked, status, wrong_counts)
        ):
            return self.P.write_preflight(
                repo_root=ROOT, evidence_root=self.evidence, context=context, **options
            )

    def read(self):
        return json.loads(self.path.read_text(encoding="utf-8"))

    def arms_blocked(self, payload):
        return sorted(arm for arm, entry in payload["arms"].items() if entry["status"] == "blocked")

    def test_it_writes_one_entry_per_distinct_catalog_key(self):
        payload, _digest = self.write()
        self.assertEqual(sorted(payload["records"]), sorted(TEN_KEYS))
        used = set()
        for spec in catalog().values():
            for key in (spec.train_key, spec.score_key, spec.beside_key):
                used.add(evidence_io.record_key_str(key))
        self.assertEqual(set(payload["records"]), used)
        for label, entry in payload["records"].items():
            with self.subTest(key=label):
                variant, fidelity, _identifier = label.split("/")
                self.assertEqual(entry["status"], "ok")
                self.assertEqual(entry["n_within_t"], EXPECTED_WITHIN_T[f"{variant}/{fidelity}"])
                self.assertEqual(entry["expected_within_t"], EXPECTED_WITHIN_T[f"{variant}/{fidelity}"])
                self.assertIs(entry["count_ok"], True)

    def test_the_file_holds_the_schema_the_counts_and_one_status_per_arm(self):
        payload, digest = self.write()
        self.assertEqual(self.read(), payload)
        self.assertEqual(self.path.read_bytes(), evidence_io.canonical_json_bytes(payload))
        self.assertEqual(digest, sha256_file(self.path))
        self.assertEqual(payload["schema"], "phase60-preflight/v1")
        self.assertEqual(payload["scorecard_sha256"], load_scorecard().sha256)
        self.assertEqual(payload["t_max"], 10.0)
        self.assertEqual(payload["data_root_source"], "synthetic")
        self.assertEqual(sorted(payload["arms"]), sorted(ALL_ARMS))
        self.assertEqual(payload["blocked_arms"], [])
        row = payload["arms"]["p2b-2279"]
        self.assertEqual(
            row,
            {
                "status": "ok",
                "train_key": "standard/base/2279",
                "score_key": "standard/gold/2279",
                "beside_key": "standard/base/2279",
                "blocked_by": [],
            },
        )

    def test_the_attestation_summary_is_embedded_and_every_open_counter_is_zero(self):
        payload, _digest = self.write()
        attestation = payload["attestation"]
        for counter in ("test_split_opened", "blocked_attempts", "refused_before_open"):
            with self.subTest(counter=counter):
                self.assertEqual(attestation[counter], 0)
        self.assertEqual(attestation["opened"]["train"], 10)

    def test_a_nonzero_open_counter_halts_before_anything_is_written(self):
        for counter in ("test_split_opened", "blocked_attempts", "refused_before_open"):
            with self.subTest(counter=counter):
                with self.assertRaises(HarnessHalt):
                    self.write(context=stub_context(**{counter: 1}))
                self.assertFalse(self.path.exists())

    def test_a_context_with_no_attestation_halts(self):
        context = stub_context()
        context.attestation = None
        with self.assertRaises(HarnessHalt):
            self.write(context=context)
        self.assertFalse(self.path.exists())

    def test_a_blocked_probe_key_blocks_only_the_arms_that_use_it(self):
        payload, _digest = self.write(blocked=("standard/base/2279",))
        self.assertEqual(
            self.arms_blocked(payload), ["c-p1-2279", "c-p2b-2279", "p1-2279", "p2b-2279"]
        )
        self.assertEqual(payload["arms"]["p1-2279"]["blocked_by"], ["standard/base/2279"])
        self.assertEqual(payload["arms"]["r1-1632"]["status"], "ok")
        self.assertEqual(payload["records"]["standard/base/2279"]["status"], "missing")
        self.assertIs(payload["records"]["standard/base/2279"]["count_ok"], False)

    def test_a_blocked_gold_probe_key_blocks_both_probe_arms_of_its_system(self):
        payload, _digest = self.write(blocked=("standard/gold/3418",))
        self.assertEqual(
            self.arms_blocked(payload), ["c-p1-3418", "c-p2b-3418", "p1-3418", "p2b-3418"]
        )

    def test_a_blocked_rung_1_key_blocks_every_arm_of_that_system_and_no_other(self):
        payload, _digest = self.write(blocked=("hierarchical/gold/851",))
        expected = sorted(arm for arm, spec in catalog().items() if spec.system_id == 851)
        self.assertEqual(self.arms_blocked(payload), expected)
        self.assertIn("r1-851", expected)
        self.assertEqual(payload["arms"]["r1-1632"]["status"], "ok")
        self.assertEqual(payload["arms"]["r1-4658"]["status"], "ok")

    def test_every_status_other_than_ok_blocks(self):
        for status in ("missing", "empty", "unreadable", "refused"):
            with self.subTest(status=status):
                self.path.unlink(missing_ok=True)
                payload, _digest = self.write(blocked=("hierarchical/base/4658",), status=status)
                self.assertEqual(payload["records"]["hierarchical/base/4658"]["status"], status)
                self.assertIn("r1-4658", self.arms_blocked(payload))

    def test_a_window_count_other_than_the_expected_blocks_the_arm(self):
        payload, _digest = self.write(wrong_counts=("hierarchical/gold/4658",))
        entry = payload["records"]["hierarchical/gold/4658"]
        self.assertEqual(entry["status"], "ok")
        self.assertEqual((entry["n_within_t"], entry["expected_within_t"]), (1000, 1001))
        self.assertIs(entry["count_ok"], False)
        expected = sorted(arm for arm, spec in catalog().items() if spec.system_id == 4658)
        self.assertEqual(self.arms_blocked(payload), expected)

    def test_the_data_root_never_reaches_the_file(self):
        self.write()
        text = self.path.read_text(encoding="ascii")
        self.assertNotIn(SYNTHETIC_DATA_ROOT, text)
        self.assertNotIn(str(Path.home()), text)

    def test_text_that_names_the_data_root_is_refused_and_nothing_is_written(self):
        def leaky(keys, context, *, scorecard):
            report = fake_preflight()(keys, context, scorecard=scorecard)
            first = next(iter(report))
            report[first] = {"status": "unreadable", "split": "train",
                             "message": f"cannot open {SYNTHETIC_DATA_ROOT}/file.txt"}
            return report

        with mock.patch.object(self.P, "preflight_records", leaky):
            with self.assertRaises(EvidenceRedactionError):
                self.P.write_preflight(
                    repo_root=ROOT, evidence_root=self.evidence, context=stub_context()
                )
        self.assertFalse(self.path.exists())

    def test_a_second_write_is_refused_and_the_first_file_stays(self):
        _payload, digest = self.write()
        with self.assertRaises(FirstResultExists):
            self.write(blocked=("hierarchical/base/1632",))
        self.assertEqual(sha256_file(self.path), digest)

    def test_the_real_context_is_opened_only_when_none_is_injected(self):
        opened = mock.Mock(return_value=stub_context())
        with mock.patch.object(self.P, "open_real_context", opened):
            with mock.patch.object(self.P, "preflight_records", fake_preflight()):
                self.P.write_preflight(repo_root=ROOT, evidence_root=self.evidence)
            opened.assert_called_once_with(repo_root=ROOT)
            opened.reset_mock()
            self.path.unlink()
            self.write()
            opened.assert_not_called()

    def test_a_real_reader_reports_the_mapped_records_and_substitutes_nothing(self):
        with ExitStack() as stack:
            fixture = stack.enter_context(gold_corpus_fixture())
            context = fixture_context(
                allowlist=fixture.allowlist, reader=fixture.reader, stats=fixture.stats,
                attestation=StubAttestation(),
            )
            absent = next(
                key
                for key in fixture.allowlist.records("train", variant="hierarchical", fidelity="gold")
                if not fixture.reader.exists(key)
            )
            key_map = {}
            for text in TEN_KEYS:
                variant, fidelity, identifier = text.split("/")
                key = RecordKey(variant, fidelity, int(identifier))
                if text == "standard/base/2279":
                    key_map[key] = absent
                elif fidelity == "base":
                    key_map[key] = fixture.base_key
                else:
                    key_map[key] = fixture.gold_key
            reference = self.P.preflight_records(
                [fixture.base_key, fixture.gold_key], context, scorecard=load_scorecard()
            )
            base_entry = reference[evidence_io.record_key_str(fixture.base_key)]
            gold_entry = reference[evidence_io.record_key_str(fixture.gold_key)]
            counts = {
                "hierarchical/base": base_entry["n_within_t"],
                "standard/base": base_entry["n_within_t"],
                "hierarchical/gold": gold_entry["n_within_t"],
                "standard/gold": gold_entry["n_within_t"],
            }
            with mock.patch.object(self.P, "EXPECTED_WITHIN_T", counts):
                payload, _digest = self.P.write_preflight(
                    repo_root=ROOT, evidence_root=self.evidence, context=context, key_map=key_map
                )
        self.assertEqual(sorted(payload["records"]), sorted(TEN_KEYS))
        missing = payload["records"]["standard/base/2279"]
        self.assertEqual(missing["status"], "missing")
        self.assertNotIn("windowed_sha256", missing)
        self.assertEqual(payload["records"]["hierarchical/gold/1632"]["status"], "ok")
        self.assertEqual(
            payload["records"]["hierarchical/gold/1632"]["windowed_sha256"],
            gold_entry["windowed_sha256"],
        )
        self.assertEqual(
            self.arms_blocked(payload), ["c-p1-2279", "c-p2b-2279", "p1-2279", "p2b-2279"]
        )
        self.assertNotIn(str(fixture.data_root), self.path.read_text(encoding="ascii"))


# ---------------------------------------------------------------------------
# Admission of the Rung-1 arms and the checks every arm passes.
# ---------------------------------------------------------------------------

class AdmissionRung1Tests(unittest.TestCase):
    def setUp(self):
        self.P = admission_module(self)

    def base(self, **options):
        return registered(self, "base", None, **options)

    def test_a_rung_1_arm_is_admitted_with_the_full_contract(self):
        tree = self.base()
        for arm_id in sorted(R1):
            with self.subTest(arm=arm_id):
                admission = tree.admit(arm_id)
                self.assertEqual(
                    set(admission),
                    {
                        "arm_id", "protocol_sha256", "preflight_sha256", "first_omega_0",
                        "omega_provenance", "ruling", "r_ref_in_force", "scorer_context_r_ref",
                        "s_h", "clip_enabled", "failed_confirmation_pre_answer",
                    },
                )
                self.assertEqual(admission["arm_id"], arm_id)
                self.assertEqual(admission["protocol_sha256"], sha256_file(tree.root / PROTOCOL_PATH))
                self.assertEqual(admission["preflight_sha256"], sha256_file(tree.root / PREFLIGHT_PATH))
                self.assertEqual(admission["first_omega_0"], 30.0)
                self.assertEqual(admission["omega_provenance"], "locked")
                self.assertIsNone(admission["ruling"])
                self.assertIsNone(admission["r_ref_in_force"])
                self.assertIsNone(admission["scorer_context_r_ref"])
                self.assertIsNone(admission["s_h"])
                self.assertIs(admission["clip_enabled"], True)
                self.assertIsNone(admission["failed_confirmation_pre_answer"])

    def test_at_the_start_only_the_three_rung_1_arms_are_admitted(self):
        self.assertEqual(self.base().admitted(), R1)

    def test_admission_reads_committed_files_only_and_creates_nothing(self):
        tree = self.base()
        before = subprocess.run(["git", "status", "--porcelain"], cwd=tree.root,
                                capture_output=True, text=True, check=True).stdout
        with mock.patch.object(self.P, "open_real_context", side_effect=AssertionError("opened")):
            tree.admit("r1-1632")
        after = subprocess.run(["git", "status", "--porcelain"], cwd=tree.root,
                               capture_output=True, text=True, check=True).stdout
        self.assertEqual(before, after)
        self.assertFalse((tree.root / "runs" / "phase60").exists())

    def test_an_existing_record_or_owner_stop_refuses_the_arm(self):
        for name in ("record.json", "owner-stop.json"):
            with self.subTest(file=name):
                tree = self.base()
                directory = tree.evidence / "arms" / "r1-1632"
                directory.mkdir(parents=True)
                (directory / name).write_text("{}\n", encoding="utf-8")
                tree.refusal("r1-1632", name)
                tree.admit("r1-851")

    def test_a_fresh_start_needs_no_run_directory_and_a_resume_needs_one(self):
        tree = self.base()
        run_dir = tree.root / "runs" / "phase60" / "r1-1632"
        tree.refusal("r1-1632", "resume", resume=True)
        run_dir.mkdir(parents=True)
        tree.refusal("r1-1632", "runs/phase60/r1-1632")
        admission = tree.admit("r1-1632", resume=True)
        self.assertEqual(admission["arm_id"], "r1-1632")
        tree.refusal("r1-851", "resume", resume=True)

    def test_a_resume_is_refused_after_a_record_or_an_owner_stop(self):
        tree = self.base()
        (tree.root / "runs" / "phase60" / "r1-1632").mkdir(parents=True)
        directory = tree.evidence / "arms" / "r1-1632"
        directory.mkdir(parents=True)
        (directory / "owner-stop.json").write_text("{}\n", encoding="utf-8")
        tree.refusal("r1-1632", "owner-stop.json", resume=True)

    def test_an_arm_outside_the_closed_catalog_is_refused(self):
        tree = self.base()
        for arm_id in ("r1-9999", "../r1-1632", "R1-1632", "", None, "/tmp/r1-1632", 7):
            with self.subTest(arm=arm_id):
                tree.refusal(arm_id, "catalog")

    def test_a_key_the_preflight_blocks_refuses_exactly_the_arms_that_use_it(self):
        tree = self.base(blocked=("hierarchical/gold/1632",))
        message = tree.refusal("r1-1632", "hierarchical/gold/1632")
        self.assertIn("preflight", message)
        tree.admit("r1-851")
        tree.admit("r1-4658")

    def test_a_window_count_the_preflight_flags_refuses_the_arm(self):
        tree = self.base(wrong_counts=("hierarchical/gold/851",))
        tree.refusal("r1-851", "hierarchical/gold/851")
        tree.admit("r1-1632")

    def test_every_blocked_status_refuses(self):
        for status in ("missing", "empty", "unreadable", "refused"):
            with self.subTest(status=status):
                tree = self.base(blocked=("hierarchical/base/4658",), blocked_status=status)
                tree.refusal("r1-4658", "hierarchical/base/4658", status)

    def test_a_drifted_pinned_module_refuses_every_arm_and_is_named(self):
        tree = self.base()
        target = tree.root / PLAN_PINNED[22]
        target.write_bytes(target.read_bytes() + b"\n")
        for arm_id in ("r1-1632", "r1-851"):
            with self.subTest(arm=arm_id):
                tree.refusal(arm_id, "differs", PLAN_PINNED[22])

    def test_a_drifted_recorded_input_refuses_the_arm(self):
        tree = self.base()
        edit_json(tree.root, METADATA, lambda payload: payload.update(note="changed"))
        tree.refusal("r1-1632", METADATA)

    def test_an_amendment_commit_outside_the_history_refuses_the_arm(self):
        tree = self.base(amendment="dangling")
        tree.refusal("r1-1632", "amendment", "ancestor")

    def test_an_absent_untracked_or_dirty_protocol_refuses_the_arm(self):
        tree = RegisteredTree(self)
        tree.refusal("r1-1632", "run protocol")
        tree = self.base()
        path = tree.root / PROTOCOL_PATH
        original = path.read_bytes()
        path.write_bytes(original + b" ")
        tree.refusal("r1-1632", "run protocol")
        path.write_bytes(original)
        tree.admit("r1-1632")
        subprocess.run(["git", "rm", "--cached", "-q", PROTOCOL_PATH], cwd=tree.root, check=True)
        tree.refusal("r1-1632", "run protocol")

    def test_a_missing_untracked_or_dirty_preflight_refuses_the_arm(self):
        tree = self.base()
        path = tree.root / PREFLIGHT_PATH
        original = path.read_bytes()
        path.write_bytes(original + b" ")
        tree.refusal("r1-1632", "preflight")
        path.write_bytes(original)
        subprocess.run(["git", "rm", "--cached", "-q", PREFLIGHT_PATH], cwd=tree.root, check=True)
        tree.refusal("r1-1632", "preflight")
        path.unlink()
        tree.refusal("r1-1632", "preflight")

    def test_a_preflight_other_than_the_one_the_protocol_pins_refuses_the_arm(self):
        tree = self.base()
        edit_json(tree.root, PREFLIGHT_PATH, lambda payload: payload.update(note="edited"))
        commit_all(tree.root, "edit the preflight after the protocol")
        tree.refusal("r1-1632", "preflight", "pins")

    def test_a_preflight_whose_open_counters_are_not_zero_refuses_the_arm(self):
        tree = self.base(preflight_tweak="counters")
        tree.refusal("r1-1632", "preflight", "test_split_opened")

    def test_a_scorer_or_scorecard_digest_that_the_files_do_not_match_refuses_the_arm(self):
        for tweak, word in (("scorer", "scorer"), ("scorecard", "scorecard")):
            with self.subTest(tweak=tweak):
                tree = self.base(protocol_tweak=tweak)
                tree.refusal("r1-1632", word)

    def test_a_refusal_is_one_line_and_names_no_absolute_path(self):
        tree = self.base(blocked=("hierarchical/gold/1632",))
        message = tree.refusal("r1-1632")
        self.assertNotIn(str(tree.root), message)
        self.assertNotIn(str(Path.home()), message)


# ---------------------------------------------------------------------------
# Per-branch admission.
# ---------------------------------------------------------------------------

class AdmissionBranchTests(unittest.TestCase):
    def setUp(self):
        self.P = admission_module(self)

    def test_sweep_arms_run_only_on_the_recorded_sweep_system(self):
        tree = registered(self, "fired-000", build_fired)
        self.assertEqual(tree.admitted(), G2S_1632)
        for setting in (60, 120, 240, 480):
            with self.subTest(setting=setting):
                admission = tree.admit(f"g2s-1632-w{setting:03d}")
                self.assertEqual(admission["first_omega_0"], float(setting))
                self.assertEqual(admission["omega_provenance"], "g2_sweep_override")
                self.assertIsNone(admission["ruling"])
                self.assertIsNone(admission["r_ref_in_force"])
        tree.refusal("g2s-851-w060", "sweep system 1632")
        tree.refusal("g2c-851-w120", "confirmation")
        tree.refusal("r2b-1632", "ladder")
        tree.refusal("c-r1u-4658", "ladder")

    def test_the_sweep_system_follows_the_failing_pair(self):
        tree = registered(self, "fired-100", lambda t: build_fired(t, (1, 0, 0)))
        self.assertEqual(tree.admitted(), {f"g2s-851-w{s:03d}" for s in (60, 120, 240, 480)})
        tree.refusal("g2s-1632-w060", "sweep system 851")

    def test_no_sweep_arm_runs_when_g2_did_not_fire(self):
        tree = registered(self, "quiet", lambda t: t.with_outcome((1, 1, 1)))
        tree.refusal("g2s-1632-w060", "sweep")
        tree.refusal("g2s-851-w060", "sweep")
        tree.refusal("g2c-851-w120", "confirmation")

    def test_the_confirmation_runs_only_as_the_recorded_confirmation_arm(self):
        tree = registered(self, "curve-000", build_curve)
        self.assertEqual(tree.admitted(), {"g2c-851-w120"})
        admission = tree.admit("g2c-851-w120")
        self.assertEqual(admission["first_omega_0"], 120.0)
        self.assertEqual(admission["omega_provenance"], "confirmation_override")
        tree.refusal("g2c-851-w060", "confirmation arm g2c-851-w120")
        tree.refusal("g2c-4658-w120", "confirmation arm g2c-851-w120")
        tree.refusal("g2s-1632-w060", "record.json")

    def test_the_confirmation_follows_the_failing_pair_and_the_highest_setting(self):
        grid = {60: 1, 120: 0, 240: 1, 480: 0}
        tree = registered(self, "curve-100", lambda t: build_curve(t, (1, 0, 0), grid))
        self.assertEqual(tree.admitted(), {"g2c-4658-w240"})

    def test_a_curve_with_no_tier_one_setting_admits_no_confirmation(self):
        tree = registered(self, "curve-none", lambda t: build_curve(t, (0, 0, 0), ZERO_GRID))
        self.assertEqual(tree.admitted(), set())
        tree.refusal("g2c-851-w120", "confirmation")
        tree.refusal("r2b-1632", "ladder")

    def test_the_stop_path_admits_nothing_and_a_skip_record_refuses_every_ladder_arm(self):
        tree = registered(self, "stopped", build_stop)
        self.assertEqual(tree.admitted(), set())
        for arm_id in sorted(LADDER | CONTINUE_LADDER | {"c-r1u-4658"}):
            with self.subTest(arm=arm_id):
                tree.refusal(arm_id)

    def test_when_g2_did_not_fire_the_ladder_arms_run_at_the_locked_setting(self):
        tree = registered(self, "quiet", lambda t: t.with_outcome((1, 1, 1)))
        self.assertEqual(tree.admitted(), LADDER)
        admission = tree.admit("r2b-1632")
        self.assertEqual((admission["first_omega_0"], admission["omega_provenance"]), (30.0, "locked"))
        self.assertIsNone(admission["ruling"])
        tree.refusal("c-r2b-1632", "continue")
        tree.refusal("c-r1u-4658", "continue")
        tree.refusal("g2s-1632-w060", "sweep")

    def test_an_unanswered_checkpoint_admits_no_ladder_arm(self):
        tree = registered(self, "rescued", build_rescue)
        self.assertEqual(tree.admitted(), set())
        tree.refusal("r2b-1632", "checkpoint 4")
        tree.refusal("c-r2b-1632", "checkpoint 4")

    def test_a_go_to_verdict_answer_stops_the_ladder(self):
        tree = registered(
            self, "verdict", lambda t: (build_rescue(t), t.with_checkpoint4("go-to-verdict"))
        )
        self.assertEqual(tree.admitted(), set())
        tree.refusal("c-r2b-1632")
        tree.refusal("r2b-1632")

    def test_a_continue_admits_the_continue_arms_and_only_the_recorded_uncovered_rung_1(self):
        tree = registered(self, "continue-120", build_continue("120", 120.0))
        self.assertEqual(tree.admitted(), {"c-r1u-4658"} | CONTINUE_LADDER)
        tree.refusal("c-r1u-851", "uncovered system 4658")
        tree.refusal("c-r1u-1632", "uncovered system 4658")
        tree.refusal("r2b-1632", "continue")
        tree.refusal("p1-2279", "continue")

    def test_the_continue_admission_carries_the_ruling_and_the_setting(self):
        tree = registered(self, "continue-120", build_continue("120", 120.0))
        ruling_sha = tree.ruling_sha()
        for arm_id in ("c-r2b-1632", "c-r1u-4658", "c-p1-2279", "c-p2b-3418"):
            with self.subTest(arm=arm_id):
                admission = tree.admit(arm_id)
                self.assertEqual(admission["first_omega_0"], 120.0)
                self.assertEqual(admission["omega_provenance"], "owner_approved")
                ruling = admission["ruling"]
                self.assertEqual(ruling["sha256"], ruling_sha)
                self.assertEqual(ruling["path"], RULING_PATH)
                self.assertEqual(ruling["answer"], "continue")
                self.assertEqual(ruling["approved_first_omega_0"], 120.0)
                self.assertIs(ruling["on_grid"], True)
                self.assertIs(ruling["equals_confirmed"], True)

    def test_an_approved_setting_off_the_grid_is_admitted_and_flagged(self):
        tree = registered(self, "continue-150", build_continue("150", 150.0))
        admission = tree.admit("c-r2a-851")
        self.assertEqual(admission["first_omega_0"], 150.0)
        self.assertIs(admission["ruling"]["on_grid"], False)
        self.assertIs(admission["ruling"]["equals_confirmed"], False)

    def test_an_approved_grid_setting_other_than_the_confirmed_one_says_so(self):
        tree = registered(self, "continue-240", build_continue("240", 240.0))
        admission = tree.admit("c-r2a-851")
        self.assertIs(admission["ruling"]["on_grid"], True)
        self.assertIs(admission["ruling"]["equals_confirmed"], False)

    def test_a_continue_waits_for_a_passed_re_measure_at_the_approved_setting(self):
        pending = registered(
            self, "continue-no-remeasure",
            lambda t: (build_rescue(t), t.with_checkpoint4("continue", "120")),
        )
        self.assertEqual(pending.admitted(), set())
        pending.refusal("c-r2b-1632", "re-measure")
        blocked = registered(self, "continue-block", build_continue("120", 120.0, "BLOCK"))
        self.assertEqual(blocked.admitted(), set())
        blocked.refusal("c-r2b-1632", "GATE-04 BLOCK")

    def test_a_re_measure_at_another_setting_refuses_the_continue_arms(self):
        tree = registered(self, "continue-120", build_continue("120", 120.0))
        payload = json.loads(tree.path("continue/gate04-remeasure.json").read_text(encoding="utf-8"))
        payload["first_omega_0"] = 240.0
        write_json(tree.path("continue/gate04-remeasure.json"), payload)
        tree.commit("a re-measure at another setting")
        tree.refusal("c-r2b-1632", "another setting")


# ---------------------------------------------------------------------------
# The reference in force, S_H and the clipping flag.
# ---------------------------------------------------------------------------

class ReferenceInForceTests(unittest.TestCase):
    def setUp(self):
        self.P = admission_module(self)

    def governed(self):
        return {"path": R_REF, "sha256": GOVERNED_SHA, "value": R_REF_VALUE, "note": REFERENCE_NOTE}

    def test_a_physics_arm_at_the_locked_setting_gets_the_governed_reference(self):
        tree = registered(self, "quiet", lambda t: t.with_outcome((1, 1, 1)))
        self.assertEqual(sha256_file(tree.root / R_REF), GOVERNED_SHA)
        for arm_id in ("r2a-1632", "r2b-851", "p2b-2279", "p2b-3418"):
            with self.subTest(arm=arm_id):
                admission = tree.admit(arm_id)
                self.assertEqual(admission["r_ref_in_force"], self.governed())
                self.assertEqual(
                    admission["scorer_context_r_ref"], {"path": R_REF, "sha256": GOVERNED_SHA}
                )

    def test_data_only_arms_get_no_reference(self):
        tree = registered(self, "quiet", lambda t: t.with_outcome((1, 1, 1)))
        for arm_id in ("p1-2279", "p1-3418"):
            with self.subTest(arm=arm_id):
                admission = tree.admit(arm_id)
                self.assertIsNone(admission["r_ref_in_force"])
                self.assertIsNone(admission["scorer_context_r_ref"])
                self.assertIsNone(admission["s_h"])

    def test_only_the_probe_rung_2b_arms_get_s_h_and_eps_h(self):
        tree = registered(self, "quiet", lambda t: t.with_outcome((1, 1, 1)))
        expected = {"value": S_H, "eps_h": EPS_H, "source_sha256": sha256_file(ROOT / METADATA)}
        for arm_id in ("p2b-2279", "p2b-3418"):
            with self.subTest(arm=arm_id):
                self.assertEqual(tree.admit(arm_id)["s_h"], expected)
        for arm_id in ("r2a-1632", "r2b-1632", "p1-2279"):
            with self.subTest(arm=arm_id):
                self.assertIsNone(tree.admit(arm_id)["s_h"])

    def test_a_continue_physics_arm_gets_the_re_measured_reference_and_probes_reuse_it(self):
        tree = registered(self, "continue-120", build_continue("120", 120.0))
        approved = json.loads(tree.path("continue/r-ref-approved.json").read_text(encoding="utf-8"))
        expected = {
            "path": APPROVED_PATH,
            "sha256": sha256_file(tree.path("continue/r-ref-approved.json")),
            "value": approved["r_ref"],
            "note": REFERENCE_NOTE,
        }
        self.assertNotEqual(expected["value"], R_REF_VALUE)
        for arm_id in ("c-r2a-1632", "c-r2b-4658", "c-p2b-2279", "c-p2b-3418"):
            with self.subTest(arm=arm_id):
                admission = tree.admit(arm_id)
                self.assertEqual(admission["r_ref_in_force"], expected)
                self.assertEqual(
                    admission["scorer_context_r_ref"], {"path": R_REF, "sha256": GOVERNED_SHA}
                )
        self.assertIsNotNone(tree.admit("c-p2b-3418")["s_h"])
        for arm_id in ("c-r1u-4658", "c-p1-2279"):
            with self.subTest(arm=arm_id):
                self.assertIsNone(tree.admit(arm_id)["r_ref_in_force"])

    def test_a_re_measured_reference_that_is_not_the_one_recorded_refuses_the_arm(self):
        tree = registered(self, "continue-120", build_continue("120", 120.0))
        artifact = tree.path("continue/r-ref-approved.json")
        original = artifact.read_bytes()
        artifact.write_bytes(original + b" ")
        tree.refusal("c-r2b-1632", "r-ref-approved.json")
        artifact.write_bytes(original)
        tree.admit("c-r2b-1632")
        subprocess.run(["git", "rm", "--cached", "-q", APPROVED_PATH], cwd=tree.root, check=True)
        tree.refusal("c-r2b-1632", "r-ref-approved.json")
        # A data-only continue arm does not read the re-measured reference.
        tree.admit("c-r1u-4658")

    def test_a_re_measure_record_that_cites_another_artifact_path_refuses_the_arm(self):
        tree = registered(self, "continue-120", build_continue("120", 120.0))
        payload = json.loads(tree.path("continue/gate04-remeasure.json").read_text(encoding="utf-8"))
        payload["r_ref_artifact"]["path"] = R_REF
        payload["r_ref_artifact"]["sha256"] = GOVERNED_SHA
        write_json(tree.path("continue/gate04-remeasure.json"), payload)
        tree.commit("a re-measure that cites the governed file")
        tree.refusal("c-r2b-1632", "r-ref-approved.json")

    def test_clipping_follows_the_protocol_for_data_only_arms_and_never_for_physics_arms(self):
        tree = registered(self, "quiet-noclip", lambda t: t.with_outcome((1, 1, 1)), clip=False)
        self.assertIs(tree.admit("p1-2279")["clip_enabled"], False)
        self.assertIs(tree.admit("r2b-1632")["clip_enabled"], True)
        self.assertIs(tree.admit("r2a-851")["clip_enabled"], True)
        self.assertIs(tree.admit("p2b-3418")["clip_enabled"], True)
        default = registered(self, "quiet", lambda t: t.with_outcome((1, 1, 1)))
        self.assertIs(default.admit("p1-2279")["clip_enabled"], True)

    def test_the_failed_confirmation_pre_answer_is_carried(self):
        tree = registered(
            self, "quiet-preanswer", lambda t: t.with_outcome((1, 1, 1)), pre_answer="no_rescue"
        )
        self.assertEqual(tree.admit("r2b-1632")["failed_confirmation_pre_answer"], "no_rescue")


# ---------------------------------------------------------------------------
# The command line: preflight and admit.
# ---------------------------------------------------------------------------

class CommandLineTests(unittest.TestCase):
    def setUp(self):
        self.P = admission_module(self)

    def cli(self, tree, *argv):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = self.P.main([*argv, "--evidence-root", str(tree.evidence)])
        return code, buffer.getvalue().strip()

    def test_admit_prints_the_token_and_exits_zero(self):
        tree = registered(self, "base", None)
        code, out = self.cli(tree, "admit", "r1-1632")
        self.assertEqual((code, out), (0, "ADMIT-OK r1-1632"))

    def test_a_refusal_is_one_line_with_the_reason_and_exit_two(self):
        tree = registered(self, "base", None)
        for arm_id in ("r2b-1632", "no-such-arm", "../r1-1632"):
            with self.subTest(arm=arm_id):
                code, out = self.cli(tree, "admit", arm_id)
                self.assertEqual(code, 2, out)
                self.assertTrue(out.startswith("ADMIT-REFUSED: "), out)
                self.assertEqual(len(out.splitlines()), 1)

    def test_admit_without_a_protocol_is_refused(self):
        tree = RegisteredTree(self)
        code, out = self.cli(tree, "admit", "r1-1632")
        self.assertEqual(code, 2, out)
        self.assertTrue(out.startswith("ADMIT-REFUSED: "), out)

    def test_preflight_writes_the_file_once_and_prints_its_hash(self):
        tree = RegisteredTree(self)
        context = stub_context()
        with mock.patch.object(self.P, "open_real_context", return_value=context), mock.patch.object(
            self.P, "preflight_records", fake_preflight()
        ):
            code, out = self.cli(tree, "preflight")
            self.assertEqual(code, 0, out)
            path = tree.root / PREFLIGHT_PATH
            self.assertEqual(
                out, f"PREFLIGHT-OK: {PREFLIGHT_PATH} sha256 {sha256_file(path)} "
                     "(10 records ok, 42 arms ok)",
            )
            code, out = self.cli(tree, "preflight")
            self.assertEqual(code, 2, out)
            self.assertTrue(out.startswith("PREFLIGHT-REFUSED: "), out)

    def test_preflight_reports_blocked_arms_but_still_records_them(self):
        tree = RegisteredTree(self)
        with mock.patch.object(self.P, "open_real_context", return_value=stub_context()), \
                mock.patch.object(self.P, "preflight_records",
                                  fake_preflight(blocked=("standard/base/3418",))):
            code, out = self.cli(tree, "preflight")
        self.assertEqual(code, 2, out)
        self.assertTrue(out.startswith("PREFLIGHT-BLOCKED: 4 arms blocked"), out)
        payload = json.loads((tree.root / PREFLIGHT_PATH).read_text(encoding="utf-8"))
        self.assertEqual(payload["blocked_arms"], ["c-p1-3418", "c-p2b-3418", "p1-3418", "p2b-3418"])

    def test_preflight_halts_on_a_nonzero_attestation_counter(self):
        tree = RegisteredTree(self)
        with mock.patch.object(
            self.P, "open_real_context", return_value=stub_context(test_split_opened=2)
        ), mock.patch.object(self.P, "preflight_records", fake_preflight()):
            code, out = self.cli(tree, "preflight")
        self.assertEqual(code, 2, out)
        self.assertTrue(out.startswith("PREFLIGHT-REFUSED: "), out)
        self.assertFalse((tree.root / PREFLIGHT_PATH).exists())


if __name__ == "__main__":
    unittest.main()
