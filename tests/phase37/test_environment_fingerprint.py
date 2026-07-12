"""Phase 37 ENV-02 canonical fingerprint, lock-hash, secret-minimization, and
non-overwrite test contract (CTX-06 / CTX-07 / T-37-04).

Wave 0 contract. Tests import ``scripts.verify_environment`` inside test
methods so module compilation is the only Wave 0 green condition.
"""

import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
VERIFY_PY = ROOT / "scripts" / "verify_environment.py"
REQUIREMENTS_LOCK = ROOT / "requirements-lock.txt"


# CTX-06 fingerprint allowlist. Every field the canonical JSON object MUST
# carry. The Markdown rendering is derived from the same in-memory object.
REQUIRED_FIELDS = (
    "schema_version",
    "timestamp",
    "repository_commit",
    "platform",        # structured: sw_vers + arch
    "conda",           # conda prefix / version
    "python",          # python version
    "packages",        # torch / numpy / h5py / yaml / tensorboard
    "torch",           # build / mps_available / device_count
    "lock",            # path + sha256 of exact replay bytes
    "verification",    # structured check results
)

# Canary secrets injected into the fixture environment. The fingerprint must
# never serialize any of these — neither under a key match nor under a generic
# environment/configuration dump.
SECRET_CANARIES = {
    "GITHUB_TOKEN": "ghp_PHASE37_CANARY_TOKEN_DO_NOT_LEAK",
    "AWS_SECRET_ACCESS_KEY": "AKIAPHASE37CANARY",
    "CONDA_TOKEN": "phase37-conda-canary",
    "PINN_API_KEY": "phase37-api-canary",
    "SSH_PASSPHRASE": "phase37-ssh-canary",
}

# Substrings that must never appear in either fingerprint rendering.
SECRET_SUBSTRINGS = tuple(SECRET_CANARIES.values()) + (
    "CANARY",
    "ghp_",
    "AKIA",
)


class EnvironmentFingerprintTests(unittest.TestCase):
    """Hermetic CTX-06 / CTX-07 fingerprint schema, hashing, and non-overwrite tests."""

    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp(prefix="phase37-fingerprint-"))
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _load_verify_module(self):
        if not VERIFY_PY.exists():
            self.skipTest("scripts/verify_environment.py not implemented until Wave 1")
        # Import the module from file path without polluting sys.modules across
        # tests; the import is the deliberate Wave-0->Wave-1 RED->green hinge.
        import importlib.util
        spec = importlib.util.spec_from_file_location("verify_environment", str(VERIFY_PY))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_canonical_json_uses_sorted_keys_fixed_indentation_and_final_newline(self):
        # CTX-06: canonical JSON is sorted-key, UTF-8, fixed indentation, with a
        # final newline. Two calls over the same object must produce byte-identical
        # output.
        module = self._load_verify_module()
        if not hasattr(module, "canonical_json_bytes"):
            self.skipTest("canonical_json_bytes not yet exported")
        obj = {
            "zeta": 1,
            "alpha": {"b": 2, "a": 3},
            "nested": [{"y": 1, "x": 0}],
        }
        first = module.canonical_json_bytes(obj)
        second = module.canonical_json_bytes(obj)
        self.assertEqual(first, second, "canonical_json_bytes is not deterministic")
        self.assertTrue(first.endswith(b"\n"), "canonical JSON missing final newline")
        text = first.decode("utf-8")
        # Keys must appear in sorted order at every level.
        self.assertLess(text.index('"alpha"'), text.index('"nested"'))
        self.assertLess(text.index('"nested"'), text.index('"zeta"'))
        self.assertIn('"a": 3', text)
        self.assertIn('"x": 0', text)

    def test_sha256_file_hashes_exact_bytes(self):
        # CTX-06: the lock hash is over exact bytes. Two files with the same
        # content but different names hash identically; a single-byte change
        # hashes differently.
        module = self._load_verify_module()
        if not hasattr(module, "sha256_file"):
            self.skipTest("sha256_file not yet exported")
        a = self.tmp / "a.txt"
        b = self.tmp / "b.txt"
        a.write_bytes(b"phase37 lock content\n")
        b.write_bytes(b"phase37 lock content\n")
        self.assertEqual(module.sha256_file(a), module.sha256_file(b))
        b.write_bytes(b"phase37 lock content\r\n")  # single-byte change
        self.assertNotEqual(module.sha256_file(a), module.sha256_file(b))

    def test_render_fingerprint_markdown_is_derived_from_same_object(self):
        # CTX-06: the Markdown rendering must be derived from the same canonical
        # object as the JSON, not from a parallel code path.
        module = self._load_verify_module()
        if not hasattr(module, "render_fingerprint_markdown"):
            self.skipTest("render_fingerprint_markdown not yet exported")
        canonical_obj = {
            "schema_version": "phase37/v1",
            "timestamp": "2026-07-12T00:00:00Z",
            "repository_commit": "0" * 40,
            "platform": {"os": "macOS", "version": "15.0", "arch": "arm64"},
            "conda": {"prefix": "/tmp/conda"},
            "python": "3.11.x",
            "packages": {"torch": "2.12.0"},
            "torch": {"mps_available": True, "device_count": 1, "build": "test"},
            "lock": {"path": "requirements-lock.txt", "sha256": "x" * 64},
            "verification": {"python_3_11": True, "torch_2_12": True, "imports": True,
                             "pip_check": True, "lock_match": True, "mps_available": True},
        }
        json_bytes = module.canonical_json_bytes(canonical_obj)
        md = module.render_fingerprint_markdown(canonical_obj)
        # Every top-level key in the canonical object must be reflected in the
        # Markdown rendering.
        for key in canonical_obj:
            self.assertIn(key, md, f"Markdown rendering missing canonical key {key}")
        # Both renderings must come from the same object: changing the object
        # changes both.
        canonical_obj["python"] = "3.11.9"
        md2 = module.render_fingerprint_markdown(canonical_obj)
        self.assertNotEqual(md, md2, "Markdown rendering ignores canonical object mutations")

    def test_fingerprint_includes_all_required_ctx06_fields(self):
        module = self._load_verify_module()
        if not hasattr(module, "write_fingerprint_pair"):
            self.skipTest("write_fingerprint_pair not yet exported")
        # write_fingerprint_pair must reject an object missing any required field.
        for missing in REQUIRED_FIELDS:
            obj = {k: "x" for k in REQUIRED_FIELDS}
            obj.pop(missing)
            with self.assertRaises((ValueError, KeyError, TypeError),
                                   msg=f"write_fingerprint_pair accepted missing {missing}"):
                module.write_fingerprint_pair(obj, self.tmp)

    def test_fingerprint_excludes_all_secret_canaries(self):
        # T-37-04: fingerprint output must never contain injected secrets, under
        # any key. The verifier must read only from its allowlist.
        module = self._load_verify_module()
        if not hasattr(module, "write_fingerprint_pair"):
            self.skipTest("write_fingerprint_pair not yet exported")
        # Build a minimal valid object that references every required field but
        # does not include secrets; verify secrets injected into os.environ are
        # not pulled in.
        obj = {
            "schema_version": "phase37/v1",
            "timestamp": "2026-07-12T00:00:00Z",
            "repository_commit": "0" * 40,
            "platform": {"os": "macOS", "version": "15.0", "arch": "arm64"},
            "conda": {"prefix": "/tmp/conda"},
            "python": "3.11.9",
            "packages": {"torch": "2.12.0", "numpy": "2.x", "h5py": "3.x",
                         "yaml": "6.x", "tensorboard": "2.x"},
            "torch": {"mps_available": True, "device_count": 1, "build": "test"},
            "lock": {"path": "requirements-lock.txt", "sha256": "x" * 64},
            "verification": {"python_3_11": True, "torch_2_12": True, "imports": True,
                             "pip_check": True, "lock_match": True, "mps_available": True},
        }
        out_dir = self.tmp / "run1"
        # Inject canaries into the test process env; the verifier must not read them.
        saved = {}
        for k, v in SECRET_CANARIES.items():
            saved[k] = os.environ.get(k)
            os.environ[k] = v
        try:
            module.write_fingerprint_pair(obj, out_dir)
        finally:
            for k, v in saved.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
        json_text = (out_dir / "fingerprint.json").read_text()
        md_text = (out_dir / "fingerprint.md").read_text()
        for needle in SECRET_SUBSTRINGS:
            self.assertNotIn(needle, json_text, f"secret canary leaked into JSON: {needle}")
            self.assertNotIn(needle, md_text, f"secret canary leaked into Markdown: {needle}")

    def test_check_only_mode_writes_no_evidence(self):
        # CTX-06: --check-only succeeds or fails without writing any fingerprint.
        if not VERIFY_PY.exists():
            self.skipTest("scripts/verify_environment.py not implemented until Wave 1")
        out_dir = self.tmp / "checkonly"
        env = dict(os.environ)
        proc = subprocess.run(
            [sys.executable, str(VERIFY_PY), "--check-only",
             "--output-root", str(out_dir)],
            cwd=ROOT, env=env, capture_output=True, text=True, check=False,
            timeout=30,
        )
        # Whether it passed or failed (host may lack pinn-train), it must not
        # have written a fingerprint.
        self.assertFalse(out_dir.exists() or any(out_dir.glob("**/*")),
                         "check-only mode wrote evidence")

    def test_exclusive_run_ids_collision_preserved(self):
        # CTX-07: evidence runs are non-overwriting. Two runs with the same ID
        # must collide and preserve the first run's bytes.
        module = self._load_verify_module()
        if not hasattr(module, "write_fingerprint_pair"):
            self.skipTest("write_fingerprint_pair not yet exported")
        obj_a = {
            "schema_version": "phase37/v1", "timestamp": "2026-07-12T00:00:00Z",
            "repository_commit": "0" * 40,
            "platform": {"os": "macOS", "arch": "arm64"},
            "conda": {}, "python": "3.11.9", "packages": {}, "torch": {},
            "lock": {"path": "l", "sha256": "x" * 64}, "verification": {},
        }
        obj_b = dict(obj_a)
        obj_b["timestamp"] = "2026-07-13T00:00:00Z"
        run_dir = self.tmp / "20260712T000000Z"
        module.write_fingerprint_pair(obj_a, run_dir)
        first_json = (run_dir / "fingerprint.json").read_bytes()
        # Collision must not overwrite.
        with self.assertRaises((FileExistsError, OSError, ValueError)):
            module.write_fingerprint_pair(obj_b, run_dir)
        self.assertEqual(first_json, (run_dir / "fingerprint.json").read_bytes(),
                         "collision overwrote the first run's bytes")


if __name__ == "__main__":
    unittest.main()
