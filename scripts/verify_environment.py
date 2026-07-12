#!/usr/bin/env python3
"""scripts/verify_environment.py — Phase 37 / ENV-02 runtime verifier and
canonical environment provenance writer (CTX-06 / CTX-07 / T-37-04).

Public API (the Wave 0 contract in tests/phase37/test_environment_fingerprint.py):
    sha256_file(path) -> str
    canonical_json_bytes(obj) -> bytes
    verify_environment(lock_file) -> dict   # the canonical fingerprint object
    render_fingerprint_markdown(obj) -> str
    write_fingerprint_pair(obj, out_dir) -> None  # exclusive, atomic, non-overwrite

CLI:
    verify_environment.py [--check-only] [--lock-file PATH] [--output-root DIR]

    --check-only     Validate the runtime contract; write NO evidence.
    --lock-file PATH Path to requirements-lock.txt (default: repo-root).
    --output-root DIR  Root directory for exclusive timestamped run dirs.

Exit code: 0 on success (or --check-only success), non-zero on any verification
failure. Prints exactly two lines on a non-check-only success:
    FINGERPRINT_JSON=<absolute path>
    FINGERPRINT_MARKDOWN=<absolute path>
"""

import argparse
import datetime as _dt
import hashlib
import json
import os
import pathlib
import platform
import subprocess
import sys
import tempfile

SCHEMA_VERSION = "phase37/v1"
REQUIRED_PACKAGES = ("torch", "numpy", "h5py", "yaml", "tensorboard")
REQUIRED_PYTHON_MAJOR = 3
REQUIRED_PYTHON_MINOR = 11
REQUIRED_TORCH_MAJOR = 2
REQUIRED_TORCH_MINOR = 12

# CTX-06 fingerprint field allowlist. Every top-level key the canonical object
# MUST carry. write_fingerprint_pair rejects an object missing any of these.
REQUIRED_FIELDS = (
    "schema_version",
    "timestamp",
    "repository_commit",
    "platform",
    "conda",
    "python",
    "packages",
    "torch",
    "lock",
    "verification",
)

# Substrings that must never appear in any fingerprint rendering. Tested by
# tests/phase37/test_environment_fingerprint.py (T-37-04 secret canaries).
_FORBIDDEN_SUBSTRINGS = (
    "GITHUB_TOKEN", "ghp_", "AKIA", "AWS_SECRET",
    "CONDA_TOKEN", "API_KEY", "SSH_PASSPHRASE", "CANARY",
)


def sha256_file(path):
    """Return the hex SHA-256 of a file's exact bytes."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json_bytes(obj):
    """Deterministic UTF-8 JSON: sorted keys, 2-space indent, final newline."""
    text = json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False)
    return (text + "\n").encode("utf-8")


def _run_capture(argv, env=None, timeout=60):
    """Run a command, return CompletedProcess with captured text."""
    return subprocess.run(
        [str(a) for a in argv],
        capture_output=True, text=True, env=env, check=False, timeout=timeout,
    )


def _repo_root():
    return pathlib.Path(__file__).resolve().parents[1]


def _git_commit():
    proc = _run_capture(
        ["git", "-C", str(_repo_root()), "rev-parse", "HEAD"],
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
    )
    if proc.returncode != 0:
        return "unknown"
    return proc.stdout.strip() or "unknown"


def _sw_vers():
    proc = _run_capture(["sw_vers"])
    # sw_vers emits "ProductName:\t\tmacOS", "ProductVersion:\t\t26.5.1",
    # "BuildVersion:\t\t25F80". Map the camelCase keys to our snake_case
    # field names explicitly (no spaces in sw_vers keys, so a generic
    # .replace(" ","_") would not match).
    key_map = {
        "productname": "product_name",
        "productversion": "product_version",
        "buildversion": "build_version",
    }
    fields = {"product_name": "", "product_version": "", "build_version": ""}
    if proc.returncode == 0:
        for line in proc.stdout.splitlines():
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip().lower()
            value = value.strip()
            if key in key_map:
                fields[key_map[key]] = value
    return fields


def _platform_facts():
    return {
        "os": platform.system(),
        "machine": platform.machine(),
        "sw_vers": _sw_vers(),
    }


def _conda_facts(python_exe):
    """Discover conda prefix/version from the running Python's environment."""
    # Prefer CONDA_PREFIX (set inside `conda run`), fall back to marching up
    # from the python executable to find a conda-meta directory.
    prefix = os.environ.get("CONDA_PREFIX", "")
    conda_exe = os.environ.get("CONDA_EXE", "")
    version = os.environ.get("CONDA_VERSION", "")
    if not prefix:
        # March up from python_exe to find .../envs/<name> or a base prefix.
        py = pathlib.Path(python_exe).resolve()
        for parent in [py.parent, *py.parents]:
            if (parent / "conda-meta").is_dir():
                prefix = str(parent)
                break
    return {"prefix": prefix, "executable": conda_exe, "version": version}


def _python_facts():
    return ".".join(str(v) for v in sys.version_info[:3])


def _package_versions():
    versions = {}
    for name in REQUIRED_PACKAGES:
        try:
            if name == "yaml":
                import yaml
                versions["PyYAML"] = getattr(yaml, "__version__", "unknown")
            else:
                mod = __import__(name)
                versions[name] = getattr(mod, "__version__", "unknown")
        except Exception as exc:
            versions[name] = f"IMPORT_ERROR: {exc}"
    return versions


def _torch_facts():
    try:
        import torch
        return {
            "version": torch.__version__,
            "build": getattr(torch.version, "build", None) or "unknown",
            "git_version": getattr(torch.version, "git_version", "unknown"),
            "is_debug": bool(torch.version.is_debug) if hasattr(torch.version, "is_debug") else False,
            "mps": {
                "is_built": bool(torch.backends.mps.is_built()),
                "is_available": bool(torch.backends.mps.is_available()),
                "device_count": int(getattr(torch.mps, "device_count", lambda: 1)()),
            },
        }
    except Exception as exc:
        return {"import_error": str(exc)}


def _pip_check_ok():
    """Return (ok, output). Runs `python -m pip check` in the current env."""
    proc = _run_capture([sys.executable, "-m", "pip", "check"])
    return proc.returncode == 0, proc.stdout + proc.stderr


def _installed_match_lock(lock_file):
    """Return (ok, installed_dict). installed_dict maps 'name==ver' lines."""
    proc = _run_capture([sys.executable, "-m", "pip", "freeze", "--all"])
    if proc.returncode != 0:
        return False, {}
    installed = {}
    for line in proc.stdout.splitlines():
        line = line.strip()
        if "==" in line:
            name, _, ver = line.partition("==")
            installed[name.strip().lower()] = ver.strip()
    lock = {}
    for line in pathlib.Path(lock_file).read_text().splitlines():
        line = line.strip()
        if "==" in line:
            name, _, ver = line.partition("==")
            lock[name.strip().lower()] = ver.strip()
    # Every locked package must be installed at the exact locked version.
    for name, ver in lock.items():
        if installed.get(name) != ver:
            return False, installed
    return True, installed


def verify_environment(lock_file):
    """Build the canonical fingerprint object and run all verification checks.

    Returns the canonical object (always populated, even on failure, so the
    caller can inspect what was observed). The caller inspects
    obj['verification']['status'] and the individual check booleans.
    """
    lock_file = pathlib.Path(lock_file).resolve()
    python_version = _python_facts()
    packages = _package_versions()
    torch_facts = _torch_facts()
    conda_facts = _conda_facts(sys.executable)
    pip_check_ok, pip_check_output = _pip_check_ok()
    installed_match, _installed = _installed_match_lock(lock_file)

    # Individual checks.
    py_ok = (sys.version_info.major == REQUIRED_PYTHON_MAJOR
             and sys.version_info.minor == REQUIRED_PYTHON_MINOR)
    torch_version = torch_facts.get("version", "")
    torch_ok = (torch_version.startswith(f"{REQUIRED_TORCH_MAJOR}.{REQUIRED_TORCH_MINOR}.")
                and "import_error" not in torch_facts)
    imports_ok = all("IMPORT_ERROR" not in v for v in packages.values())
    mps_ok = bool(torch_facts.get("mps", {}).get("is_available", False))

    checks = {
        "python_3_11": bool(py_ok),
        "torch_2_12": bool(torch_ok),
        "required_imports": bool(imports_ok),
        "pip_check": bool(pip_check_ok),
        "lock_match": bool(installed_match),
        "mps_available": bool(mps_ok),
    }
    status = "pass" if all(checks.values()) else "fail"

    obj = {
        "schema_version": SCHEMA_VERSION,
        "timestamp": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository_commit": _git_commit(),
        "platform": _platform_facts(),
        "conda": conda_facts,
        "python": python_version,
        "packages": packages,
        "torch": torch_facts,
        "lock": {
            "path": str(lock_file.relative_to(_repo_root())) if str(lock_file).startswith(str(_repo_root())) else str(lock_file),
            "sha256": sha256_file(lock_file) if lock_file.exists() else "MISSING",
        },
        "verification": {
            "status": status,
            "checks": checks,
        },
    }
    if not pip_check_ok and pip_check_output.strip():
        # Carry a bounded diagnostic so the owner can see why pip check failed,
        # without dumping the whole environment (CTX-06 / T-37-04 secrecy).
        obj["verification"]["pip_check_tail"] = pip_check_output.strip().splitlines()[-5:]
    return obj


def render_fingerprint_markdown(obj):
    """Render the canonical object as owner-readable Markdown.

    Derived from the same in-memory object as the JSON (not a parallel path).
    Contains only allowlisted fields plus the fixed provenance statement.
    """
    lines = []
    lines.append("# Environment Fingerprint")
    lines.append("")
    lines.append(f"- **schema_version:** `{obj['schema_version']}`")
    lines.append(f"- **timestamp:** {obj['timestamp']}")
    lines.append(f"- **repository_commit:** `{obj['repository_commit']}`")
    pf = obj.get("platform", {})
    lines.append(f"- **platform.os:** {pf.get('os','')}")
    lines.append(f"- **platform.machine:** {pf.get('machine','')}")
    sw = pf.get("sw_vers", {}) or {}
    lines.append(f"- **platform.sw_vers:** {sw.get('product_name','')} {sw.get('product_version','')} ({sw.get('build_version','')})")
    cf = obj["conda"]
    lines.append(f"- **conda.prefix:** `{cf.get('prefix','')}`")
    lines.append(f"- **conda.version:** {cf.get('version','') or 'unknown'}")
    lines.append(f"- **python:** {obj['python']}")
    lines.append("- **packages:**")
    for name, ver in sorted(obj["packages"].items()):
        lines.append(f"  - `{name}=={ver}`")
    tf = obj["torch"]
    mps = tf.get("mps", {})
    lines.append(f"- **torch.version:** {tf.get('version','unknown')}")
    lines.append(f"- **torch.build:** {tf.get('build','unknown')}")
    lines.append(f"- **torch.mps.is_built:** {mps.get('is_built', False)}")
    lines.append(f"- **torch.mps.is_available:** {mps.get('is_available', False)}")
    lines.append(f"- **torch.mps.device_count:** {mps.get('device_count', 0)}")
    lk = obj["lock"]
    lines.append(f"- **lock.path:** `{lk.get('path','')}`")
    lines.append(f"- **lock.sha256:** `{lk.get('sha256','')}`")
    v = obj["verification"]
    lines.append(f"- **verification.status:** {v.get('status','unknown')}")
    lines.append("- **verification.checks:**")
    for name, ok in sorted(v.get("checks", {}).items()):
        lines.append(f"  - `{name}`: {'pass' if ok else 'FAIL'}")
    return "\n".join(lines) + "\n"


def _assert_no_secrets(text, where):
    for needle in _FORBIDDEN_SUBSTRINGS:
        if needle in text:
            raise ValueError(
                f"fingerprint {where} contains forbidden substring {needle!r} — "
                "refusing to serialize a potential secret")


def write_fingerprint_pair(obj, out_dir, run_id=None):
    """Write canonical JSON + derived Markdown.

    Two call patterns:
      * ``write_fingerprint_pair(obj, run_dir)`` — writes ``fingerprint.json``
        and ``fingerprint.md`` directly into ``run_dir``. The caller owns the
        run directory's exclusivity/naming. Collision (existing dir) is a hard
        error.
      * ``write_fingerprint_pair(obj, root, run_id="<id>")`` — creates
        ``root/<run_id>`` exclusively and writes into it. ``run_id`` must be a
        single path component (no separators / traversal).

    Atomic: each file is written via a sibling temp + os.replace.
    Rejects objects missing any REQUIRED_FIELDS key.
    """
    for field in REQUIRED_FIELDS:
        if field not in obj:
            raise KeyError(f"fingerprint object missing required field {field!r}")
    out_dir = pathlib.Path(out_dir)
    if run_id is None:
        # Caller owns the run directory; write directly into out_dir.
        run_dir = out_dir
    else:
        # Reject separators / traversal in the run_id.
        if any(c in run_id for c in ("/", "\\", "..", os.sep)) or run_id != pathlib.Path(run_id).name:
            raise ValueError(f"run_id contains separators or traversal: {run_id!r}")
        run_dir = out_dir / run_id
    if run_dir.exists():
        raise FileExistsError(f"fingerprint run directory already exists: {run_dir}")
    # Exclusive create.
    run_dir.mkdir(parents=True, exist_ok=False)

    json_bytes = canonical_json_bytes(obj)
    md_text = render_fingerprint_markdown(obj)
    # Secret-canary scan before we write either rendering.
    _assert_no_secrets(json_bytes.decode("utf-8"), "JSON")
    _assert_no_secrets(md_text, "Markdown")

    _atomic_write_bytes(run_dir / "fingerprint.json", json_bytes)
    _atomic_write_bytes(run_dir / "fingerprint.md", md_text.encode("utf-8"))
    return run_dir


def _atomic_write_bytes(path, data):
    """Sibling temp + fsync + os.replace."""
    path = pathlib.Path(path)
    tmp = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def _emit_paths(run_dir):
    """Print the canonical FINGERPRINT_JSON / FINGERPRINT_MARKDOWN lines."""
    print(f"FINGERPRINT_JSON={pathlib.Path(run_dir, 'fingerprint.json').resolve()}")
    print(f"FINGERPRINT_MARKDOWN={pathlib.Path(run_dir, 'fingerprint.md').resolve()}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Phase 37 environment verifier")
    parser.add_argument("--check-only", action="store_true",
                        help="validate without writing evidence")
    parser.add_argument("--lock-file", default=str(_repo_root() / "requirements-lock.txt"),
                        help="path to requirements-lock.txt")
    parser.add_argument("--output-root",
                        default=str(_repo_root() / ".planning"
                                    / "phases"
                                    / "37-developer-environment-precision-adjudication"
                                    / "evidence" / "environment"),
                        help="root directory for exclusive timestamped run dirs")
    args = parser.parse_args(argv)

    lock_file = pathlib.Path(args.lock_file).resolve()
    if not lock_file.exists():
        print(f"verify_environment: lock file not found: {lock_file}", file=sys.stderr)
        return 2

    obj = verify_environment(lock_file)
    status = obj["verification"]["status"]
    if status != "pass":
        # Always report the failing checks to stderr before exiting.
        print("verify_environment: verification FAILED:", file=sys.stderr)
        for name, ok in obj["verification"]["checks"].items():
            if not ok:
                print(f"  FAIL: {name}", file=sys.stderr)
        return 1

    if args.check_only:
        # --check-only succeeds without writing any evidence.
        print("verify_environment: check-only PASS (no evidence written)")
        return 0

    # Normal path: write a new exclusive fingerprint pair under a UTC run_id.
    run_id = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = write_fingerprint_pair(obj, pathlib.Path(args.output_root), run_id=run_id)
    _emit_paths(run_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
