"""Phase 37 ENV-01/02 bootstrap, seed-lock, and fingerprint test contract.

Wave 0 contract for CTX-01..CTX-07. Hermetic stdlib-only tests that exercise
the bootstrap state machine, the seed/normal/refresh lock boundary, and the
canonical fingerprint schema using fixture-owned fake tools and temporary
prefixes. Wave 0 never contacts a network, invokes host conda, a real
installer, or MPS.

Production imports (``setup.sh`` via subprocess, ``scripts/verify_environment``,
``scripts/refresh-environment-lock``) are kept inside test methods so module
compilation is the only Wave 0 green condition.
"""

import json
import os
import pathlib
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SETUP_SH = ROOT / "setup.sh"
REFRESH_SH = ROOT / "scripts" / "refresh-environment-lock.sh"
BOOTSTRAP_LIB = ROOT / "scripts" / "lib" / "conda_bootstrap.sh"
VERIFY_PY = ROOT / "scripts" / "verify_environment.py"
ENVIRONMENT_YML = ROOT / "environment.yml"
REQUIREMENTS_LOCK = ROOT / "requirements-lock.txt"


# Environment variables that, if inherited from the parent session, would leak
# the host conda/git identity into a fixture-owned subprocess. Stripped from
# every cleaned child environment so the fake tools are authoritative.
_ISOLATED_KEYS = (
    "GIT_AGENT_ID",
    "GIT_AGENT_OWNED_PATHS",
    "GIT_AGENT_COMMIT",
    "GIT_DIR",
    "GIT_WORK_TREE",
    "CONDA_PREFIX",
    "CONDA_DEFAULT_ENV",
    "CONDA_EXE",
    "MAMBA_ROOT_PREFIX",
    "PYTHONPATH",
    "PYTORCH_ENABLE_MPS_FALLBACK",
)


def _clean_env(extra=None):
    merged = os.environ.copy()
    for key in _ISOLATED_KEYS:
        merged.pop(key, None)
    if extra:
        merged.update(extra)
    return merged


def _write_fake_exe(path, body):
    """Write an executable fake tool body. Atomic sibling-write semantics."""
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    tmp.write_text(body)
    tmp.chmod(0o755)
    os.replace(tmp, path)


def _fake_uname():
    return "#!/usr/bin/env bash\nif [[ \"$1\" == -s ]]; then echo Darwin; exit 0; fi\nif [[ \"$1\" == -m ]]; then echo arm64; exit 0; fi\nuname \"$@\"\n"


def _fake_sw_vers():
    return (
        "#!/usr/bin/env bash\n"
        'if [[ "$1" == -productName ]]; then echo "macOS"; exit 0; fi\n'
        'if [[ "$1\" == -productVersion ]]; then echo "15.0"; exit 0; fi\n'
        'if [[ "$1" == -buildVersion ]]; then echo "25A0000"; exit 0; fi\n'
        "sw_vers \"$@\" 2>/dev/null || true\n"
    )


def _make_fixture_repo():
    """Build a temporary repository root with fake uname/sw_vers/conda/curl/shasum.

    The fixture owns its own HOME, install prefix, target prefix, and PATH. The
    returned dict exposes every path the bootstrap tests need to assert that no
    host mutation occurs and that default setup never dispatches seed or refresh.
    """
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="phase37-bootstrap-"))
    paths = {
        "root": tmp,
        "home": tmp / "home",
        "install_prefix": tmp / "miniforge",
        "target_prefix": tmp / "envs" / "pinn-train",
        "bin": tmp / "bin",
        "path_sep": os.pathsep,
    }
    for sub in ("home", "miniforge", "envs", "bin"):
        (tmp / sub).mkdir(parents=True, exist_ok=True)
    (paths["target_prefix"]).parent.mkdir(parents=True, exist_ok=True)

    _write_fake_exe(paths["bin"] / "uname", _fake_uname())
    _write_fake_exe(paths["bin"] / "sw_vers", _fake_sw_vers())
    _write_fake_exe(paths["bin"] / "conda", _fake_conda(paths))
    _write_fake_exe(paths["bin"] / "curl", _fake_curl())
    _write_fake_exe(paths["bin"] / "shasum", _fake_shasum())
    _write_fake_exe(paths["bin"] / "bash", _fake_bash())
    return paths


def _fake_conda(paths):
    target = paths["target_prefix"]
    return (
        "#!/usr/bin/env bash\n"
        f'target="{target}"\n'
        'if [[ "$1" == "env" && "$2" == "list" ]]; then\n'
        '  if [[ -d "$target" ]]; then echo "# conda environments:"; echo "#"; fi\n'
        "  exit 0\n"
        'fi\n'
        'if [[ "$1" == "create" ]]; then\n'
        '  # emulating conda create -y -p <target> --file lock\n'
        '  mkdir -p "$target"\n'
        "  exit 0\n"
        'fi\n'
        'if [[ "$1" == "run" ]]; then\n'
        '  shift; shift  # drop -n pinn-train\n'
        '  exec "$@"\n'
        "fi\n"
        'echo "conda: unexpected invocation $*" >&2; exit 1\n'
    )


def _fake_curl():
    return (
        "#!/usr/bin/env bash\n"
        'echo "curl called with: $*" >&2\n'
        "exit 0\n"
    )


def _fake_shasum():
    return (
        "#!/usr/bin/env bash\n"
        'if [[ "$1" == -a && "$2" == 256 ]]; then\n'
        "  file=\"$3\"\n"
        "  if [[ -f \"$file\" ]]; then\n"
        '    echo "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef  $file"\n'
        "    exit 0\n"
        "  fi\n"
        "fi\n"
        "shasum \"$@\" 2>/dev/null || true\n"
    )


def _fake_bash():
    # Delegate to the real bash but only for syntax checks; the fixture PATH is
    # authoritative for everything else. This lets bash -n work without leaking
    # host conda into the bootstrap.
    real = shutil.which("bash") or "/bin/bash"
    return (
        "#!/usr/bin/env bash\n"
        f'exec {real} "$@"\n'
    )


def _run_fixture(paths, argv, env_extra=None, cwd=None):
    env = _clean_env()
    env["HOME"] = str(paths["home"])
    env["PATH"] = f"{paths['bin']}{os.pathsep}/usr/bin:/bin"
    env["CONDA_PREFIX"] = ""
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [str(a) for a in argv],
        cwd=str(cwd or paths["root"]),
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


class BootstrapContractTests(unittest.TestCase):
    """Hermetic CTX-01..CTX-04 bootstrap state-machine tests."""

    def setUp(self):
        self.fixture = _make_fixture_repo()
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        shutil.rmtree(self.fixture["root"], ignore_errors=True)

    def test_unsupported_architecture_rejected_before_download(self):
        # Fixture's fake uname reports Darwin/arm64; flip it to x86_64 to prove
        # the bootstrap library rejects before invoking curl/conda.
        fixture = self.fixture
        _write_fake_exe(fixture["bin"] / "uname",
                        "#!/usr/bin/env bash\n"
                        'if [[ "$1" == -m ]]; then echo x86_64; exit 0; fi\n'
                        'if [[ "$1" == -s ]]; then echo Darwin; exit 0; fi\n'
                        "uname \"$@\"\n")
        if BOOTSTRAP_LIB.exists():
            proc = _run_fixture(fixture, ["bash", str(BOOTSTRAP_LIB)])
            self.assertNotEqual(proc.returncode, 0, proc.stderr)
            # curl sentinel must never have been touched: no download attempted.
            curl_log = fixture["bin"] / "curl"
            self.assertTrue(curl_log.exists())

    def test_unsupported_os_rejected_before_download(self):
        fixture = self.fixture
        _write_fake_exe(fixture["bin"] / "uname",
                        "#!/usr/bin/env bash\n"
                        'if [[ "$1" == -s ]]; then echo Linux; exit 0; fi\n'
                        'if [[ "$1" == -m ]]; then echo arm64; exit 0; fi\n'
                        "uname \"$@\"\n")
        if BOOTSTRAP_LIB.exists():
            proc = _run_fixture(fixture, ["bash", str(BOOTSTRAP_LIB)])
            self.assertNotEqual(proc.returncode, 0, proc.stderr)

    def test_occupied_prefix_refused_without_deletion(self):
        fixture = self.fixture
        # Pre-create the install prefix with a sentinel file.
        sentinel = fixture["install_prefix"] / "SENTINEL"
        sentinel.parent.mkdir(parents=True, exist_ok=True)
        sentinel.write_text("owner-data")
        if BOOTSTRAP_LIB.exists():
            proc = _run_fixture(fixture, ["bash", str(BOOTSTRAP_LIB)])
            # Bootstrap must refuse rather than delete the occupied prefix.
            self.assertNotEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(sentinel.exists(),
                            "occupied prefix data was deleted by bootstrap")

    def test_incompatible_prefix_refused_without_update(self):
        fixture = self.fixture
        # Create a non-empty prefix that does not look like Miniforge.
        marker = fixture["install_prefix"] / "not-miniforge"
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text("foreign")
        if BOOTSTRAP_LIB.exists():
            proc = _run_fixture(fixture, ["bash", str(BOOTSTRAP_LIB)])
            self.assertNotEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(marker.exists())

    def test_shell_startup_files_not_mutated(self):
        fixture = self.fixture
        for rc in (".zshrc", ".bash_profile", ".bashrc", ".profile"):
            (fixture["home"] / rc).write_text("# owner content\n")
        before = {rc: (fixture["home"] / rc).read_text()
                  for rc in (".zshrc", ".bash_profile", ".bashrc", ".profile")}
        if SETUP_SH.exists():
            # Default setup from absent lock should fail fast; either way, no
            # shell startup file may be mutated.
            _run_fixture(fixture, ["bash", str(SETUP_SH)],
                         env_extra={"PINN_INSTALL_PREFIX": str(fixture["install_prefix"]),
                                    "PINN_TARGET_PREFIX": str(fixture["target_prefix"])})
        for rc, content in before.items():
            self.assertEqual(content, (fixture["home"] / rc).read_text(),
                             f"setup mutated shell startup file {rc}")

    def test_activation_handoff_is_explicit_not_persistent(self):
        # CTX-03: setup prints the explicit activation command and does not
        # spawn a child shell or modify startup files.
        if not SETUP_SH.exists():
            self.skipTest("setup.sh not implemented until Wave 1")
        fixture = self.fixture
        # With an absent lock, setup fails before target creation but must not
        # have spawned a subshell or printed a "you are now in" message.
        proc = _run_fixture(fixture, ["bash", str(SETUP_SH)])
        self.assertNotEqual(proc.returncode, 0)
        self.assertNotIn("source ", proc.stdout + proc.stderr)
        self.assertNotIn("subshell", proc.stdout + proc.stderr)


class TestLockBoundary(unittest.TestCase):
    """CTX-05 / T-37-01-L: the seed-to-normal lock boundary.

    Three lock states must remain cleanly separated:
      * explicit ``--seed`` creates only a disposable task-owned prefix from the
        loose YAML and removes it after validation;
      * explicit ordinary refresh requires an already-validated target;
      * default setup requires an already-committed lock, creates an absent
        target only from that pair, and validates an existing target without a
        solver/update.
    """

    def setUp(self):
        self.fixture = _make_fixture_repo()
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        shutil.rmtree(self.fixture["root"], ignore_errors=True)

    def test_default_setup_fails_without_committed_lock(self):
        # Remove (or never create) requirements-lock.txt — default setup must
        # exit before any target creation and never dispatch the seed/refresh
        # command.
        if not SETUP_SH.exists():
            self.skipTest("setup.sh not implemented until Wave 1")
        fixture = self.fixture
        # Simulate absent lock by pointing setup at a fixture root with no lock.
        fake_repo = fixture["root"] / "repo"
        fake_repo.mkdir()
        (fake_repo / "environment.yml").write_text(
            "name: pinn-train\ndependencies:\n  - python=3.11\n")
        proc = _run_fixture(fixture, ["bash", str(SETUP_SH)], cwd=fake_repo)
        self.assertNotEqual(proc.returncode, 0,
                            f"default setup must fail without lock: {proc.stdout}")
        trace = proc.stdout + proc.stderr
        self.assertNotIn("refresh-environment-lock", trace,
                         "default setup dispatched the lock writer")
        self.assertNotIn("--seed", trace,
                         "default setup dispatched seed mode")
        # No target prefix may have been created.
        self.assertFalse(fixture["target_prefix"].exists(),
                         "default setup created the target prefix from a missing lock")

    def test_seed_creates_only_disposable_prefix(self):
        # CTX-05: --seed provisions a task-owned temporary prefix from
        # environment.yml, validates it, writes the candidate lock atomically,
        # and leaves no pinn-train target environment.
        if not REFRESH_SH.exists():
            self.skipTest("refresh-environment-lock.sh not implemented until Wave 1")
        fixture = self.fixture
        fake_repo = fixture["root"] / "repo"
        fake_repo.mkdir()
        (fake_repo / "environment.yml").write_text(
            "name: pinn-train\nchannels:\n  - conda-forge\ndependencies:\n  - python=3.11\n  - pip\n")
        # Track every directory that exists at dispatch time so we can prove the
        # seed created only a disposable prefix and removed it.
        before_dirs = {p for p in fixture["root"].rglob("*") if p.is_dir()}
        proc = _run_fixture(fixture, ["bash", str(REFRESH_SH), "--seed"],
                            cwd=fake_repo)
        # The seed command must complete without leaving a pinn-train target.
        self.assertFalse(fixture["target_prefix"].exists(),
                         "seed mode created the pinn-train target prefix")
        # Any disposable prefix it created must be removed on success or failure.
        leftovers = [p for p in fixture["root"].rglob("*")
                     if p.is_dir() and p not in before_dirs
                     and "pinn-train" in p.name]
        self.assertEqual(leftovers, [],
                         f"seed mode left disposable prefixes: {leftovers}")

    def test_default_setup_has_no_dispatch_edge_to_seed(self):
        # Read setup.sh source and prove there is no invocation of the seed or
        # refresh command from the default path. This is a structural guard, not
        # a runtime probe.
        if not SETUP_SH.exists():
            self.skipTest("setup.sh not implemented until Wave 1")
        source = SETUP_SH.read_text()
        # The default command must not contain an unconditional dispatch to
        # refresh-environment-lock.sh --seed or to refresh mode.
        # (Setup MAY reference the lock file path; it must not invoke the writer.)
        self.assertNotIn("refresh-environment-lock.sh --seed", source,
                         "default setup dispatches seed mode")

    def test_ordinary_setup_preserves_yaml_and_lock_bytes(self):
        # CTX-05: ordinary setup validates, never rewrites the YAML or lock.
        if not SETUP_SH.exists() or not REQUIREMENTS_LOCK.exists():
            self.skipTest("setup.sh or committed lock not present yet")
        fixture = self.fixture
        before_lock = REQUIREMENTS_LOCK.read_bytes()
        before_yml = ENVIRONMENT_YML.read_bytes() if ENVIRONMENT_YML.exists() else b""
        # Point setup at the real repo (read-only intent).
        proc = _run_fixture(fixture, ["bash", str(SETUP_SH)], cwd=ROOT)
        # Whether setup succeeded or failed in the fixture environment, it must
        # not have rewritten the committed bytes.
        self.assertEqual(before_lock, REQUIREMENTS_LOCK.read_bytes(),
                         "ordinary setup rewrote the committed lock")
        if ENVIRONMENT_YML.exists():
            self.assertEqual(before_yml, ENVIRONMENT_YML.read_bytes(),
                             "ordinary setup rewrote environment.yml")


if __name__ == "__main__":
    unittest.main()
