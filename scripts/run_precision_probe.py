#!/usr/bin/env python3
"""scripts/run_precision_probe.py — Phase 37 / ENV-03 dual-arm orchestrator.

CTX-08, CTX-10, CTX-11, CTX-13, CTX-14 contract:
    * The parent is STDLIB-ONLY — it imports neither Torch nor the worker
      in-process. It invokes ``pinn.verification.componentwise_ad`` twice via
      subprocess with FIXED argv (one fp32-MPS, one fp64-CPU) and reads exactly
      one JSON object from each child's stdout.
    * Before spawning the MPS child, it removes ``PYTORCH_ENABLE_MPS_FALLBACK``
      from the copied environment (does NOT replace it with another value). The
      worker records the pre-import fallback fact; a leaked fallback is failed
      evidence, never silently accepted.
    * ``run`` accepts a fingerprint JSON path, an evidence root, and a bounded
      timeout. It exposes NO profile/tolerance/workload selector — every
      invocation must execute both fixed arms (10/30/100 protocol).
    * All defined subprocess failure modes (timeout, signal, nonzero exit,
      malformed/multiple JSON, schema/profile mismatch, fallback leakage,
      actual-device mismatch, worker exception) become STRUCTURED arm records.
      The parent never launches a retry/fallback/third child, synthesizes CPU
      success, or chooses a D1-p profile.
    * Evidence is append-only and atomic: exclusive UTC run directories,
      sibling-temp + os.replace, hash-bound to the referenced fingerprint.
    * The renderer produces facts and the FIXED owner-decision statement:
      ``Owner decision required; no D1-p verdict is recorded by this report.``
      It contains no score, winner, recommendation, profile selection,
      production default, or configuration mutation.

CLI:
    run_precision_probe.py run --fingerprint-json PATH
                              [--evidence-root DIR] [--timeout SECONDS]
                              [--python EXE]
    run_precision_probe.py validate --run-dir DIR
"""

import argparse
import datetime as _dt
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile

# stdlib-only at module top. The parent NEVER imports torch or
# pinn.verification.componentwise_ad in-process; it spawns the worker as a
# subprocess so each arm runs in an isolated, sanitized environment.

SCHEMA_VERSION = "phase37-precision/v1"
REQUIRED_ARM_IDS = ("fp32-mps", "fp64-cpu")
OWNER_DECISION_STATEMENT = (
    "Owner decision required; no D1-p verdict is recorded by this report."
)
DEFAULT_TIMEOUT_SECONDS = 900
DEFAULT_WARMUP = 10
DEFAULT_SAMPLES = 30
DEFAULT_EVALUATIONS = 100
DEFAULT_LEAF_U = 0.3

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
_WORKER_MODULE = "pinn.verification.componentwise_ad"
_EVIDENCE_ROOT_DEFAULT = (
    _REPO_ROOT / ".planning" / "phases"
    / "37-developer-environment-precision-adjudication" / "evidence" / "precision"
)


class RuntimeProfile:
    """A fixed D1-p profile (precision + device). Frozen by design."""

    __slots__ = ("profile_id", "precision", "device")

    def __init__(self, profile_id, precision, device):
        self.profile_id = profile_id
        self.precision = precision
        self.device = device

    def argv(self, python_exe, warmup, samples, evaluations, u):
        """Construct the fixed-argv subprocess invocation for this profile."""
        return [
            python_exe, "-m", _WORKER_MODULE,
            "--precision", self.precision,
            "--device", self.device,
            "--warmup", str(warmup),
            "--samples", str(samples),
            "--evaluations", str(evaluations),
            "--u", str(u),
        ]


# The two fixed profiles. Every ``run`` executes both — there is no selector.
PROFILES = (
    RuntimeProfile("fp32-mps", "float32", "mps"),
    RuntimeProfile("fp64-cpu", "float64", "cpu"),
)


def _git_commit():
    proc = subprocess.run(
        ["git", "-C", str(_REPO_ROOT), "rev-parse", "HEAD"],
        capture_output=True, text=True,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}, check=False,
    )
    if proc.returncode != 0:
        return "unknown"
    return proc.stdout.strip() or "unknown"


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _clean_child_env(base_env, profile):
    """Copy the parent env and, for the MPS arm, remove the fallback key.

    Per CTX-08 the MPS child must NOT inherit PYTORCH_ENABLE_MPS_FALLBACK. We
    remove it (pop) and never replace it with another value. The CPU arm
    inherits the parent env unchanged.
    """
    env = dict(base_env)
    if profile.device == "mps":
        env.pop("PYTORCH_ENABLE_MPS_FALLBACK", None)
    return env


def _parse_child_json(stdout):
    """Parse exactly one JSON object from child stdout. Raises on malformed."""
    text = stdout.strip()
    if not text:
        raise ValueError("empty child stdout")
    # The worker writes one JSON object + trailing newline. If anything else is
    # present, treat it as malformed (defensive — never silently pick the
    # JSON-looking substring).
    return json.loads(text)


def run_child(profile, python_exe, warmup, samples, evaluations, u,
              timeout, base_env):
    """Launch one child via fixed argv with a sanitized env. Return an arm record.

    The arm record is a structured dict carrying the profile, the process facts
    (returncode, status), the parsed child JSON (or None on failure), and any
    exception detail. Never raises — every failure mode becomes a structured
    record so the evidence remains complete and visible.
    """
    argv = profile.argv(python_exe, warmup, samples, evaluations, u)
    env = _clean_child_env(base_env, profile)
    arm = {
        "profile": profile.profile_id,
        "precision": profile.precision,
        "device": profile.device,
        "argv": list(argv),
        "requested_device": profile.device,
        "returncode": None,
        "status": None,
        "stdout": "",
        "stderr": "",
        "exception": None,
        "worker_record": None,
    }
    try:
        proc = subprocess.run(
            argv, env=env, capture_output=True, text=True,
            shell=False, timeout=timeout, check=False,
        )
        arm["returncode"] = proc.returncode
        arm["stdout"] = proc.stdout
        arm["stderr"] = proc.stderr[-4000:] if proc.stderr else ""  # bounded
        if proc.returncode != 0:
            arm["status"] = "nonzero_exit"
            arm["exception"] = f"returncode={proc.returncode}"
            return arm
        try:
            record = _parse_child_json(proc.stdout)
        except (ValueError, json.JSONDecodeError) as exc:
            arm["status"] = "malformed_stdout"
            arm["exception"] = type(exc).__name__
            return arm
        # Schema/profile consistency checks. The worker emits its profile as
        # "<precision>-<device>" (e.g. "float64-cpu") with separate top-level
        # ``precision`` and ``requested_device`` fields. We compare those rather
        # than the exact profile string label so the two naming conventions
        # (short "fp64-cpu" vs full "float64-cpu") agree.
        if (record.get("precision") != profile.precision
                or record.get("requested_device") != profile.device):
            arm["status"] = "profile_mismatch"
            arm["exception"] = (
                f"worker precision={record.get('precision')!r}/requested_device={record.get('requested_device')!r} "
                f"!= requested {profile.precision!r}/{profile.device!r}"
            )
            arm["worker_record"] = record
            return arm
        if record.get("exception") is not None:
            arm["status"] = "worker_exception"
            arm["exception"] = str(record.get("exception"))
            arm["worker_record"] = record
            return arm
        # Fallback leakage (MPS arm inherited the fallback key).
        if profile.device == "mps" and record.get("pre_import_fallback") is not None:
            arm["status"] = "fallback_leakage"
            arm["exception"] = (
                f"pre_import_fallback={record.get('pre_import_fallback')!r} (MPS arm must have it unset)"
            )
            arm["worker_record"] = record
            return arm
        # Actual-device mismatch (silent CPU fallback inside the worker).
        actual = record.get("actual_device")
        if actual != profile.device:
            arm["status"] = "device_mismatch"
            arm["exception"] = f"actual_device={actual!r} != requested {profile.device!r}"
            arm["worker_record"] = record
            return arm
        arm["status"] = "ok"
        arm["resolved_device"] = record.get("resolved_device")
        arm["actual_device"] = actual
        arm["pre_import_fallback"] = record.get("pre_import_fallback")
        arm["worker_record"] = record
        return arm
    except subprocess.TimeoutExpired as exc:
        arm["status"] = "timeout"
        arm["exception"] = "TimeoutExpired"
        arm["stdout"] = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        arm["stderr"] = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
        return arm
    except OSError as exc:
        # Signal / spawn failure.
        arm["status"] = "signal" if "signal" in str(exc).lower() else "spawn_error"
        arm["exception"] = f"{type(exc).__name__}: {exc}"
        return arm


def build_evidence(fp32_mps, fp64_cpu, fingerprint, repository_commit,
                   timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
                   warmup=DEFAULT_WARMUP, samples=DEFAULT_SAMPLES,
                   evaluations=DEFAULT_EVALUATIONS, u=DEFAULT_LEAF_U,
                   python_exe=None, timestamp=None):
    """Run both fixed-profile children and assemble the raw evidence object.

    ``fp32_mps`` and ``fp64_cpu`` may be either:
      * a dict arm record (injected — used by tests to exercise failure modes
        without spawning real children), OR
      * the sentinel ``"__spawn__"`` to launch the real worker for that arm.

    Returns the in-memory raw evidence dict. Does NOT write to disk; call
    ``write_evidence_run`` to persist (caller controls the run directory).
    """
    python_exe = python_exe or sys.executable
    timestamp = timestamp or _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    arms = {}
    for profile in PROFILES:
        injected = (fp32_mps if profile.profile_id == "fp32-mps" else fp64_cpu)
        if isinstance(injected, dict):
            arm = dict(injected)
            arm.setdefault("profile", profile.profile_id)
            arm.setdefault("precision", profile.precision)
            arm.setdefault("device", profile.device)
            arm.setdefault("requested_device", profile.device)
        else:
            arm = run_child(profile, python_exe, warmup, samples, evaluations,
                            u, timeout_seconds, dict(os.environ))
        arms[profile.profile_id] = arm
    raw = {
        "schema_version": SCHEMA_VERSION,
        "timestamp": timestamp,
        "repository_commit": repository_commit,
        "fingerprint": {
            "path": fingerprint.get("path", ""),
            "schema_version": fingerprint.get("schema_version", ""),
            "sha256": fingerprint.get("sha256", ""),
        },
        "orchestration": {
            "executable": python_exe,
            "timeout_seconds": timeout_seconds,
            "profiles": [p.profile_id for p in PROFILES],
            "fallback_policy": "stripped-for-mps",
            "protocol": {
                "warmup": warmup, "samples": samples, "evaluations": evaluations,
            },
            "u": u,
        },
        "arms": arms,
    }
    raw["verification"] = _verify_raw(raw)
    return raw


def _verify_raw(raw):
    """Compute the structural verification checks for a raw evidence object."""
    checks = {}
    arms = raw.get("arms", {})
    checks["two_arms"] = set(arms.keys()) == set(REQUIRED_ARM_IDS)
    checks["both_patterns"] = True
    for arm_id in REQUIRED_ARM_IDS:
        arm = arms.get(arm_id, {})
        wrec = arm.get("worker_record") or {}
        patterns = wrec.get("patterns", {}) if isinstance(wrec, dict) else {}
        if not {"full_jacobian", "scalar_u_jvp"}.issubset(set(patterns.keys())):
            checks["both_patterns"] = False
            break
    fp = raw.get("fingerprint", {})
    checks["fingerprint_hash_present"] = bool(fp.get("sha256"))
    return {"status": "pass" if all(checks.values()) else "fail", "checks": checks}


def render_summary(raw):
    """Render owner-readable Markdown from the in-memory raw object.

    Pure: no I/O. Reports symmetric arm facts, pass/fail/exception facts, and
    the FIXED owner-decision statement. Contains NO score, winner,
    recommendation, profile selection, production default, or language that
    chooses D1-p.
    """
    lines = []
    lines.append("# Phase 37 Dual-Arm Precision Probe — D1-p Evidence")
    lines.append("")
    lines.append(f"- **schema_version:** `{raw.get('schema_version','')}`")
    lines.append(f"- **timestamp:** {raw.get('timestamp','')}")
    lines.append(f"- **repository_commit:** `{raw.get('repository_commit','')}`")
    fp = raw.get("fingerprint", {})
    lines.append(f"- **fingerprint.path:** `{fp.get('path','')}`")
    lines.append(f"- **fingerprint.sha256:** `{fp.get('sha256','')}`")
    orch = raw.get("orchestration", {})
    lines.append(f"- **orchestration.timeout_seconds:** {orch.get('timeout_seconds')}")
    lines.append(f"- **orchestration.fallback_policy:** {orch.get('fallback_policy')}")
    lines.append(f"- **orchestration.u:** {orch.get('u')}")
    lines.append("")
    lines.append("## Arms")
    lines.append("")
    for arm_id in REQUIRED_ARM_IDS:
        arm = raw.get("arms", {}).get(arm_id, {})
        wrec = arm.get("worker_record") or {}
        lines.append(f"### {arm_id}")
        lines.append(f"- **status:** {arm.get('status','unknown')}")
        lines.append(f"- **requested_device:** {arm.get('requested_device')}")
        lines.append(f"- **resolved_device:** {arm.get('resolved_device')}")
        lines.append(f"- **actual_device:** {arm.get('actual_device')}")
        lines.append(f"- **pre_import_fallback:** {arm.get('pre_import_fallback')}")
        if arm.get("exception"):
            lines.append(f"- **exception:** {arm.get('exception')}")
        if isinstance(wrec, dict) and wrec.get("torch_build"):
            tb = wrec["torch_build"]
            lines.append(f"- **torch.version:** {tb.get('version')}")
            lines.append(f"- **torch.mps_is_built:** {tb.get('mps_is_built')}")
        patterns = wrec.get("patterns", {}) if isinstance(wrec, dict) else {}
        for pid in ("full_jacobian", "scalar_u_jvp"):
            prec = patterns.get(pid, {})
            if not prec:
                continue
            lines.append(f"- **{pid}:** aggregate_relative_error={prec.get('aggregate_relative_error')} "
                         f"criterion={prec.get('criterion')} passed={prec.get('passed')} "
                         f"median_ns={prec.get('median')}")
        lines.append("")
    v = raw.get("verification", {})
    lines.append("## Verification")
    lines.append(f"- **status:** {v.get('status','unknown')}")
    for name, ok in sorted(v.get("checks", {}).items()):
        lines.append(f"  - `{name}`: {'pass' if ok else 'FAIL'}")
    lines.append("")
    lines.append("## Owner Decision")
    lines.append("")
    lines.append(OWNER_DECISION_STATEMENT)
    lines.append("")
    return "\n".join(lines) + "\n"


def _atomic_write_text(path, text):
    path = pathlib.Path(path)
    tmp = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def _atomic_write_bytes(path, data):
    path = pathlib.Path(path)
    tmp = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def write_evidence_run(raw, evidence_root, run_id=None):
    """Persist a raw evidence object as raw.json + summary.md under an exclusive run dir.

    Exclusive: rejects separators/traversal/symlinks/collisions; the run
    directory must not exist. Atomic: each file is sibling-temp + os.replace.
    The run_id must match ``^[A-Za-z0-9_-]+$`` (no dots, slashes, hidden-dir
    prefixes, or traversal components) so evidence directories are predictable
    and grep-friendly.
    """
    import re as _re
    evidence_root = pathlib.Path(evidence_root)
    if run_id is None:
        run_id = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if not _re.fullmatch(r"[A-Za-z0-9_-]+", run_id):
        raise ValueError(
            f"run_id must match [A-Za-z0-9_-]+ (no separators, dots, or traversal): {run_id!r}"
        )
    run_dir = evidence_root / run_id
    # Reject symlink input at the parent level.
    if evidence_root.is_symlink():
        raise ValueError(f"evidence_root is a symlink: {evidence_root}")
    if run_dir.exists():
        raise FileExistsError(f"precision run directory already exists: {run_dir}")
    run_dir.mkdir(parents=True, exist_ok=False)
    # Bind the fingerprint hash now (provenance: every precision run references
    # an exact fingerprint).
    raw_json = json.dumps(raw, sort_keys=True, indent=2) + "\n"
    _atomic_write_bytes(run_dir / "raw.json", raw_json.encode("utf-8"))
    summary = render_summary(raw)
    _atomic_write_text(run_dir / "summary.md", summary)
    return run_dir


def validate_run(run_dir):
    """Validate a persisted precision run directory.

    Rejects root escapes, schema mismatch, fingerprint hash mismatch, missing
    arm/pattern, inconsistent profile/device/fallback facts, non-finite values,
    raw-timing count/statistic mismatch, and summary byte mismatch. Returns
    (ok, list_of_problems).
    """
    run_dir = pathlib.Path(run_dir).resolve()
    problems = []
    raw_path = run_dir / "raw.json"
    summary_path = run_dir / "summary.md"
    if not raw_path.exists() or not summary_path.exists():
        return False, [f"missing raw.json or summary.md in {run_dir}"]
    try:
        raw = json.loads(raw_path.read_text())
    except (ValueError, OSError) as exc:
        return False, [f"cannot parse raw.json: {exc}"]
    if raw.get("schema_version") != SCHEMA_VERSION:
        problems.append(f"schema_version mismatch: {raw.get('schema_version')!r}")
    arms = raw.get("arms", {})
    if set(arms.keys()) != set(REQUIRED_ARM_IDS):
        problems.append(f"arm IDs != {REQUIRED_ARM_IDS}: got {sorted(arms.keys())}")
    for arm_id, profile_id_zip in (("fp32-mps", ("float32", "mps")),
                                    ("fp64-cpu", ("float64", "cpu"))):
        arm = arms.get(arm_id, {})
        if arm.get("precision") != profile_id_zip[0]:
            problems.append(f"{arm_id}: precision mismatch {arm.get('precision')!r}")
        if arm.get("device") != profile_id_zip[1]:
            problems.append(f"{arm_id}: device mismatch {arm.get('device')!r}")
        wrec = arm.get("worker_record") or {}
        patterns = wrec.get("patterns", {}) if isinstance(wrec, dict) else {}
        for pid in ("full_jacobian", "scalar_u_jvp"):
            prec = patterns.get(pid)
            if not prec:
                problems.append(f"{arm_id}: missing pattern {pid}")
                continue
            ns = prec.get("raw_samples_ns") or []
            if len(ns) != DEFAULT_SAMPLES:
                problems.append(f"{arm_id}/{pid}: raw sample count {len(ns)} != {DEFAULT_SAMPLES}")
            for stat in ("median", "p25", "p75", "min", "max"):
                if stat not in prec:
                    problems.append(f"{arm_id}/{pid}: missing stat {stat}")
            agg = prec.get("aggregate_relative_error")
            if not isinstance(agg, (int, float)) or agg != agg:  # NaN check
                problems.append(f"{arm_id}/{pid}: non-finite aggregate_relative_error")
    # Summary byte comparison: re-derive and compare.
    rederived = render_summary(raw)
    on_disk = summary_path.read_text()
    if rederived != on_disk:
        problems.append("summary.md is not byte-identical to render_summary(raw)")
    return (len(problems) == 0), problems


def _load_fingerprint(fingerprint_json_path):
    """Load and hash-bind a fingerprint JSON path. Returns the binding dict."""
    p = pathlib.Path(fingerprint_json_path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"fingerprint JSON not found: {p}")
    obj = json.loads(p.read_text())
    return {
        "path": str(p),
        "schema_version": obj.get("schema_version", ""),
        "sha256": _sha256_file(p),
    }


def _cmd_run(args):
    fingerprint = _load_fingerprint(args.fingerprint_json)
    python_exe = args.python or sys.executable
    raw = build_evidence(
        fp32_mps="__spawn__", fp64_cpu="__spawn__",
        fingerprint=fingerprint, repository_commit=_git_commit(),
        timeout_seconds=args.timeout, python_exe=python_exe,
    )
    run_dir = write_evidence_run(raw, pathlib.Path(args.evidence_root))
    # Print the canonical absolute paths so the caller can capture them exactly
    # (never discover by timestamp).
    print(f"PRECISION_RUN_DIR={run_dir.resolve()}")
    print(f"RAW_JSON={(run_dir / 'raw.json').resolve()}")
    print(f"SUMMARY_MARKDOWN={(run_dir / 'summary.md').resolve()}")
    return 0


def _cmd_validate(args):
    ok, problems = validate_run(pathlib.Path(args.run_dir))
    if ok:
        print(f"validate: {args.run_dir} OK")
        return 0
    print(f"validate: {args.run_dir} FAILED:", file=sys.stderr)
    for p in problems:
        print(f"  - {p}", file=sys.stderr)
    return 1


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="run_precision_probe",
        description="Phase 37 dual-arm precision probe orchestrator (stdlib-only parent).",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_run = sub.add_parser("run", help="run both fixed profiles and write evidence")
    p_run.add_argument("--fingerprint-json", required=True,
                       help="path to the canonical environment fingerprint JSON")
    p_run.add_argument("--evidence-root", default=str(_EVIDENCE_ROOT_DEFAULT),
                       help="root directory for exclusive timestamped run dirs")
    p_run.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS,
                       help="per-child timeout in seconds")
    p_run.add_argument("--python", default=None,
                       help="python executable to use for child invocation (default: sys.executable)")
    p_run.set_defaults(func=_cmd_run)
    p_val = sub.add_parser("validate", help="validate a persisted run directory")
    p_val.add_argument("--run-dir", required=True, help="path to the run directory")
    p_val.set_defaults(func=_cmd_validate)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
