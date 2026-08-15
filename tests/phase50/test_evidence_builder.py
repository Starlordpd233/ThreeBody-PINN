"""Normal extract/source-manifest fixture tests for Plan 50-07 Task 1."""
from __future__ import annotations

import json
import os
import re
import tempfile
import unittest
from pathlib import Path

from tests.phase50._evidence_fixtures import (
    BUILDER,
    LEDGER_REL,
    REPO_ROOT,
    SOURCE_MANIFEST_REL,
    VERIFIER,
    clone_complete,
    fail_closed_message,
    sha256_file,
)


LEDGER_JSON_RE = re.compile(r"```json\n(.*?)\n```", re.S)


def load_ledger(repo: Path) -> dict:
    text = (repo / LEDGER_REL).read_text(encoding="utf-8")
    return json.loads(LEDGER_JSON_RE.search(text).group(1))


class ExtractManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.fx = clone_complete(Path(self.tmp.name) / "complete")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_complete_generation_extracts_and_verifies_three_hash_manifest(self) -> None:
        extracted = self.fx.extract()
        self.assertEqual(extracted.returncode, 0, extracted.stderr)
        verified = self.fx.verify("manifest", ["--manifest", str(SOURCE_MANIFEST_REL)])
        self.assertEqual(verified.returncode, 0, verified.stderr)
        self.assertIn("MANIFEST-OK", verified.stdout)
        manifest = json.loads(self.fx.path(SOURCE_MANIFEST_REL).read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema"], "phase50-evidence-source-manifest/v1")
        self.assertEqual(manifest["band_generation"], 4)
        self.assertIn("band_git_head", manifest)
        self.assertIn("extraction_git_head", manifest)
        self.assertNotEqual(manifest["band_git_head"], manifest["extraction_git_head"])
        ledger = load_ledger(self.fx.root)
        required_sources = []
        for record in ledger["records"]:
            if int(record["band_generation"]) != 4:
                continue
            required_sources.extend(record.get("terminal_artifact_sha256", {}))
        copied = {entry["source"] for entry in manifest["files"].values()}
        for record in ledger["records"]:
            if int(record["band_generation"]) != 4:
                continue
            artifact_dir = record["artifact_dir"]
            for rel in record["terminal_artifact_sha256"]:
                if rel.startswith("checkpoints/"):
                    continue
                source = f"{artifact_dir}/{rel}"
                self.assertIn(source, copied, f"missing ledger source {source}")
        seen = []
        for dest, entry in manifest["files"].items():
            self.assertEqual(entry["ledger_sha256"], entry["source_sha256"], dest)
            self.assertEqual(entry["source_sha256"], entry["copy_sha256"], dest)
            self.assertRegex(entry["copy_sha256"], r"^[0-9a-f]{64}$")
            seen.append(dest)
        self.assertEqual(seen, sorted(set(seen)))

    def test_escaping_source_fails_closed_and_writes_no_manifest(self) -> None:
        outside = Path(self.tmp.name) / "escape.txt"
        outside.write_text("escaped\n", encoding="utf-8")
        ledger_path = self.fx.path(LEDGER_REL)
        text = ledger_path.read_text(encoding="utf-8")
        ledger_path.write_text(
            text.replace(
                '"artifact_dir": "runs/stage0-rerun-seed42"',
                '"artifact_dir": "../escape-dir"',
                1,
            ),
            encoding="utf-8",
        )
        extracted = self.fx.extract()
        self.assertNotEqual(extracted.returncode, 0)
        self.assertIn("FAIL-CLOSED", fail_closed_message(extracted))
        self.assertFalse(self.fx.path(SOURCE_MANIFEST_REL).exists())

    def test_duplicate_source_fails_closed(self) -> None:
        ledger_path = self.fx.path(LEDGER_REL)
        text = ledger_path.read_text(encoding="utf-8")
        ledger_path.write_text(
            text.replace(
                '"launch_transcript": ".planning/phases/50-valid-stage-0-re-run/evidence/launch-transcripts/stage0-rerun-seed42-attempt-01-invocation-01-train.txt"',
                '"launch_transcript": "runs/stage0-rerun-seed42/config.yaml"',
                1,
            ),
            encoding="utf-8",
        )
        extracted = self.fx.extract()
        self.assertNotEqual(extracted.returncode, 0)
        self.assertFalse(self.fx.path(SOURCE_MANIFEST_REL).exists())

    def test_symlink_source_fails_closed(self) -> None:
        run_dir = self.fx.attempt_roots["stage0-rerun-seed42"]
        target = run_dir / "summary.json"
        linked = run_dir / "summary-link.json"
        os.symlink(target, linked)
        ledger_path = self.fx.path(LEDGER_REL)
        text = ledger_path.read_text(encoding="utf-8")
        ledger_path.write_text(
            text.replace(
                '"summary.md":',
                '"summary-link.json": "' + sha256_file(target) + '",\n        "summary.md":',
                1,
            ),
            encoding="utf-8",
        )
        extracted = self.fx.extract()
        self.assertNotEqual(extracted.returncode, 0)
        self.assertFalse(self.fx.path(SOURCE_MANIFEST_REL).exists())

    def test_missing_required_source_fails_closed(self) -> None:
        (self.fx.attempt_roots["stage0-rerun-seed41"] / "status.json").unlink()
        extracted = self.fx.extract()
        self.assertNotEqual(extracted.returncode, 0)
        self.assertFalse(self.fx.path(SOURCE_MANIFEST_REL).exists())

    def test_null_required_hash_fails_closed(self) -> None:
        ledger_path = self.fx.path(LEDGER_REL)
        text = ledger_path.read_text(encoding="utf-8")
        digest = sha256_file(self.fx.attempt_roots["stage0-rerun-seed43"] / "status.json")
        ledger_path.write_text(text.replace(f'"{digest}"', "null", 1), encoding="utf-8")
        extracted = self.fx.extract()
        self.assertNotEqual(extracted.returncode, 0)
        self.assertFalse(self.fx.path(SOURCE_MANIFEST_REL).exists())

    def test_resumed_invocation_fails_in_normal_mode(self) -> None:
        ledger_path = self.fx.path(LEDGER_REL)
        text = ledger_path.read_text(encoding="utf-8")
        ledger_path.write_text(
            text.replace('"launch_kind": "fresh"', '"launch_kind": "resume"', 1),
            encoding="utf-8",
        )
        extracted = self.fx.extract()
        self.assertNotEqual(extracted.returncode, 0)
        self.assertFalse(self.fx.path(SOURCE_MANIFEST_REL).exists())

    def test_held_out_evaluation_fails_closed(self) -> None:
        eval_dir = self.fx.attempt_roots["stage0-rerun-seed42"] / "evaluation"
        eval_dir.mkdir()
        (eval_dir / "metrics.json").write_text("{}\n", encoding="utf-8")
        extracted = self.fx.extract()
        self.assertNotEqual(extracted.returncode, 0)
        self.assertFalse(self.fx.path(SOURCE_MANIFEST_REL).exists())

    def test_checkpoint_bytes_are_hashed_not_copied(self) -> None:
        extracted = self.fx.extract()
        self.assertEqual(extracted.returncode, 0, extracted.stderr)
        verified = self.fx.verify("manifest", ["--manifest", str(SOURCE_MANIFEST_REL)])
        self.assertEqual(verified.returncode, 0, verified.stderr)
        manifest = json.loads(self.fx.path(SOURCE_MANIFEST_REL).read_text(encoding="utf-8"))
        copied_names = [Path(dest).name for dest in manifest["files"]]
        self.assertNotIn("best.pt", copied_names)
        self.assertTrue(any(entry.get("role") == "checkpoint-hash" for entry in manifest["files"].values()))
        self.assertTrue((self.fx.attempt_roots["stage0-rerun-seed42"] / "run_start_rng.pt").is_file())

    def test_mixed_identity_fails_closed(self) -> None:
        ledger_path = self.fx.path(LEDGER_REL)
        text = ledger_path.read_text(encoding="utf-8")
        ledger_path.write_text(
            text.replace('"band_generation": 4', '"band_generation": 3', 1),
            encoding="utf-8",
        )
        extracted = self.fx.extract()
        self.assertNotEqual(extracted.returncode, 0)
        self.assertFalse(self.fx.path(SOURCE_MANIFEST_REL).exists())

    def test_real_terminal_builder_still_refuses_without_writing_normal_artifacts(self) -> None:
        proc = __import__("subprocess").run(
            [__import__("sys").executable, str(BUILDER), "extract", "--repo-root", str(REPO_ROOT)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("final_band_generation is null", fail_closed_message(proc))
        self.assertFalse((REPO_ROOT / SOURCE_MANIFEST_REL).exists())


if __name__ == "__main__":
    unittest.main()
