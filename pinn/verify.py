"""Phase 43 / ACC-01 — ``python -m pinn.verify`` pre-flight ladder.

The single command an operator runs before committing the machine to a long
training run. It **orchestrates** the verification probes Phases 37/38 already
built; it adds no physics of its own and changes no model, loss, data, or
training-loop code (SPEC Prohibition: "MUST NOT build new probes, change the
model/loss/data/loop").

The ladder, in the SPEC-declared order:

    1. ``device_sanity``       — MPS availability + ``pinn.runtime.resolve_runtime``
    2. ``componentwise_ad``    — §10.3 componentwise-AD probe (both AD patterns)
    3. ``gradcheck_fp64_cpu``  — residual gradcheck, always on the fp64-CPU arm
    4. ``residual_ground_truth``— dual-gate residual on a read-only Brutus fixture
    5. ``overfit_single_trajectory`` — single-trajectory data-path overfit

Every rung is an **in-process library call** (CTX-70): the probes' own
``python -m pinn.verification.<probe>`` CLIs are never shelled out to, because a
subprocess loses the structured per-rung record and complicates the single
marker write. Every rung is individually guarded: an exception, an unimportable
probe module, and a missing probe symbol all become that rung's FAIL — never a
silent skip. The ladder always runs all five rungs so the operator sees the full
picture, and the overall verdict names the FIRST failed rung.

Marker contract (CTX-71). Both a green and a red ladder atomically write
``runs/.verify/latest-marker.json`` through ``pinn.training.atomic_io``. The
marker carries a UTC timestamp, the ordered rung records, and a fingerprint of
the runtime **and the code**::

    {"device", "dtype", "torch_version", "python_version",
     "git_head", "git_head_available"}

``marker_is_green_and_fresh`` — the predicate plan 43-04's >30-min launch gate
consumes — is fail-closed: it requires a green verdict, an age inside the
declared window, and an exact match on *every* fingerprint value. A marker
written when ``git rev-parse HEAD`` was unavailable records
``git_head_available: false`` and can never authorize a long run, because the
code it certified cannot be identified.
"""

from __future__ import annotations

import argparse
import importlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Sequence

from pinn.training.atomic_io import atomic_write_text

# --- ladder identity -------------------------------------------------------

RUNG_DEVICE_SANITY = "device_sanity"
RUNG_COMPONENTWISE_AD = "componentwise_ad"
RUNG_GRADCHECK = "gradcheck_fp64_cpu"
RUNG_RESIDUAL = "residual_ground_truth"
RUNG_OVERFIT = "overfit_single_trajectory"

#: The ordered ladder (SPEC requirement 1 / CTX-70). Order is load-bearing:
#: the overall verdict names the first failure in THIS sequence.
LADDER: tuple[str, ...] = (
    RUNG_DEVICE_SANITY,
    RUNG_COMPONENTWISE_AD,
    RUNG_GRADCHECK,
    RUNG_RESIDUAL,
    RUNG_OVERFIT,
)

# The production arm (D1-p): fp32 on MPS. ``--precision``/``--device`` override
# it for a CPU-only diagnostic pass; the two pairs ``resolve_runtime`` accepts
# are ("float32", "mps") and ("float64", "cpu").
DEFAULT_PRECISION = "float32"
DEFAULT_DEVICE = "mps"

# Rung 3 is defined on the fp64-CPU escape-hatch arm and is never run elsewhere
# (``run_gradcheck`` itself refuses any other pair).
GRADCHECK_PRECISION = "float64"
GRADCHECK_DEVICE = "cpu"

# The Phase-38 canonical read-only fixture used by rungs 4 and 5.
DEFAULT_VARIANT = "standard_quasi_random_gold_standard"
DEFAULT_TRAJECTORY_ID = "0000"

# --- marker contract -------------------------------------------------------

MARKER_SCHEMA_VERSION = "phase43-verify-marker/v1"

_FINGERPRINT_KEYS = frozenset(
    {
        "device",
        "dtype",
        "torch_version",
        "python_version",
        "git_head",
        "git_head_available",
    }
)

#: Marker location, relative to the runs root. Kept under ``runs/`` (gitignored,
#: already the home of every run-produced artifact).
MARKER_RELATIVE_PATH = Path(".verify") / "latest-marker.json"

#: Overridable for tests, mirroring ``pinn.train._RUNS_ROOT``.
_RUNS_ROOT: Path = Path("runs")

#: Freshness window for the >30-min launch gate. The window is a secondary
#: control — the full runtime+code fingerprint is the primary one — so a day is
#: long enough to be workable and short enough that an unattended machine change
#: (OS/driver-level) does not silently ride along.
DEFAULT_MAX_MARKER_AGE_S = 24 * 60 * 60

#: Bound on the ``git rev-parse HEAD`` subprocess so a wedged git can never hang
#: a verify run.
_GIT_TIMEOUT_S = 10.0

VERDICT_GREEN = "green"
VERDICT_RED = "red"


# ---------------------------------------------------------------------------
# Probe loading — a missing module or symbol is a rung FAIL, never a skip.
# ---------------------------------------------------------------------------


def _load_probe(module_name: str, symbol: str) -> Callable[..., Any]:
    """Import ``module_name`` and return ``symbol``, raising if either is absent.

    Both failure modes propagate to :func:`_record_rung`, which converts them
    into that rung's FAIL record (CTX-70: "a missing/broken probe counts as that
    rung's FAIL, never a silent skip").
    """
    module = importlib.import_module(module_name)
    if not hasattr(module, symbol):
        raise AttributeError(
            f"probe symbol {module_name}.{symbol} is missing "
            f"(broken or partially-installed probe)"
        )
    return getattr(module, symbol)


# ---------------------------------------------------------------------------
# The five rungs. Each returns ``(passed, reason)``; ``reason`` is None on PASS.
# ---------------------------------------------------------------------------


def _mps_materialization_error() -> Optional[str]:
    """Constructive MPS proof: materialize a tensor on the device, no predicate.

    GAP-43-01 (RESOLVED-WITH-INSTRUCTION, Option A): Phase 38's global
    prohibition scan rejects availability probes in later ``pinn/`` modules,
    so the proof that the MPS runtime works is *building on it* — strictly
    stronger than the banned predicate (an available-but-broken backend
    fails here too).
    """
    import torch

    try:
        probe = torch.zeros(1, device="mps")
    except Exception as exc:  # noqa: BLE001 — any raise means MPS is unusable
        return (
            "MPS probe tensor failed to materialize — the MPS runtime this "
            f"machine trains on is unusable ({type(exc).__name__}: {exc})"
        )
    if probe.device.type != "mps":
        return (
            "MPS probe tensor landed on "
            f"{probe.device.type!r} instead of 'mps' (silent fallback)"
        )
    return None


def _rung_device_sanity(precision: str, device: str) -> tuple[bool, Optional[str]]:
    """MPS materialization proof + the D1-p-resolved dtype/device landing.

    ``pinn.runtime.resolve_runtime`` deliberately does NOT inspect availability
    (CTX-12..14), so the constructive MPS check lives here rather than being
    pushed into that seam.
    """
    import torch

    from pinn.runtime import resolve_runtime

    mps_error = _mps_materialization_error()
    if mps_error is not None:
        return False, mps_error
    spec = resolve_runtime(precision, device)  # raises on an unsupported pair
    probe = torch.zeros(1, dtype=spec.dtype, device=spec.torch_device)
    if probe.device.type != spec.torch_device.type:
        return False, (
            f"requested device {spec.torch_device.type!r} but the tensor "
            f"landed on {probe.device.type!r} (silent fallback)"
        )
    if probe.dtype != spec.dtype:
        return False, (
            f"requested dtype {spec.dtype!r} but the tensor materialized as "
            f"{probe.dtype!r}"
        )
    return True, None


def _rung_componentwise_ad(precision: str, device: str) -> tuple[bool, Optional[str]]:
    """§10.3 componentwise-AD probe.

    ``run_probe_arm`` has NO top-level pass flag: PASS is every pattern's own
    ``passed`` AND a null ``exception``.
    """
    run_probe_arm = _load_probe("pinn.verification.componentwise_ad", "run_probe_arm")
    record = run_probe_arm(precision, device)
    exception = record.get("exception")
    if exception is not None:
        return False, f"probe raised inside run_probe_arm: {exception}"
    patterns = record.get("patterns") or {}
    if not patterns:
        return False, "probe returned no AD pattern records"
    failed = sorted(name for name, p in patterns.items() if not p.get("passed"))
    if failed:
        return False, f"AD pattern(s) outside the §10.3 criterion: {', '.join(failed)}"
    return True, None


def _rung_gradcheck() -> tuple[bool, Optional[str]]:
    """Residual gradcheck — always the fp64-CPU arm, whatever the requested arm."""
    run_gradcheck = _load_probe("pinn.verification.gradcheck_probe", "run_gradcheck")
    record = run_gradcheck(GRADCHECK_PRECISION, GRADCHECK_DEVICE)
    if record.get("passed"):
        return True, None
    reason = record.get("reason") or "torch.autograd.gradcheck reported FAIL"
    exception = record.get("exception")
    if exception is not None:
        reason = f"{reason} ({exception})"
    return False, reason


def _rung_residual(
    precision: str, device: str, variant: str, trajectory_id: str
) -> tuple[bool, Optional[str]]:
    """Dual-gate residual on one read-only ground-truth Brutus trajectory."""
    run_residual = _load_probe(
        "pinn.verification.residual_probe", "run_residual_on_ground_truth"
    )
    record = run_residual(precision, device, variant=variant, id=trajectory_id)
    if record.get("passed"):
        return True, None
    failed_gates = [
        gate
        for gate in ("gate_a", "gate_b")
        if not (record.get(gate) or {}).get("passed")
    ]
    detail = ", ".join(failed_gates) if failed_gates else "unspecified gate"
    return False, f"residual gate(s) failed on {variant}/{trajectory_id}: {detail}"


def _rung_overfit(
    precision: str,
    device: str,
    variant: str,
    trajectory_id: str,
    max_steps: Optional[int],
) -> tuple[bool, Optional[str]]:
    """Single-trajectory data-path overfit (the probe's own >=1e3x loss gate)."""
    run_overfit = _load_probe("pinn.verification.overfit_probe", "run_overfit")
    kwargs: dict[str, Any] = {"variant": variant, "id": trajectory_id}
    if max_steps is not None:
        kwargs["max_steps"] = int(max_steps)
    record = run_overfit(precision, device, **kwargs)
    if record.get("passed"):
        return True, None
    reason = record.get("fail_reason") or "overfit probe reported FAIL"
    return False, f"overfit on {variant}/{trajectory_id}: {reason}"


def _record_rung(
    name: str, call: Callable[[], tuple[bool, Optional[str]]]
) -> dict[str, Any]:
    """Run one rung, converting any exception into that rung's FAIL record."""
    try:
        passed, reason = call()
    except Exception as exc:  # noqa: BLE001 — a raising rung is a FAIL, not a crash
        return {
            "name": name,
            "passed": False,
            "reason": f"{type(exc).__name__}: {exc}",
        }
    if passed:
        return {"name": name, "passed": True, "reason": None}
    return {"name": name, "passed": False, "reason": reason or "rung reported FAIL"}


def run_ladder(
    *,
    precision: str = DEFAULT_PRECISION,
    device: str = DEFAULT_DEVICE,
    variant: str = DEFAULT_VARIANT,
    trajectory_id: str = DEFAULT_TRAJECTORY_ID,
    overfit_max_steps: Optional[int] = None,
) -> list[dict[str, Any]]:
    """Run all five rungs in order and return their ordered records.

    Every rung runs even after an earlier failure, so one invocation reports the
    whole environment rather than only its first problem. Each record is
    ``{"name", "passed", "reason"}`` and is JSON-serializable as-is.
    """
    calls: dict[str, Callable[[], tuple[bool, Optional[str]]]] = {
        RUNG_DEVICE_SANITY: lambda: _rung_device_sanity(precision, device),
        RUNG_COMPONENTWISE_AD: lambda: _rung_componentwise_ad(precision, device),
        RUNG_GRADCHECK: _rung_gradcheck,
        RUNG_RESIDUAL: lambda: _rung_residual(
            precision, device, variant, trajectory_id
        ),
        RUNG_OVERFIT: lambda: _rung_overfit(
            precision, device, variant, trajectory_id, overfit_max_steps
        ),
    }
    return [_record_rung(name, calls[name]) for name in LADDER]


def ladder_is_green(results: Sequence[Mapping[str, Any]]) -> bool:
    """True only when every rung in the ladder passed."""
    records = list(results)
    if len(records) != len(LADDER):
        return False
    return all(bool(record.get("passed")) for record in records)


def _marker_ladder_is_valid(rungs: Any) -> bool:
    """Require the exact ordered ladder and strict-boolean green results."""
    if not isinstance(rungs, Sequence) or isinstance(rungs, (str, bytes)):
        return False
    records = list(rungs)
    if len(records) != len(LADDER):
        return False
    if not all(isinstance(record, Mapping) for record in records):
        return False
    if [record.get("name") for record in records] != list(LADDER):
        return False
    return all(record.get("passed") is True for record in records)


def first_failed_rung(results: Sequence[Mapping[str, Any]]) -> Optional[str]:
    """Name of the earliest failing rung in ladder order, or None if green."""
    for record in results:
        if not record.get("passed"):
            return str(record.get("name"))
    return None


# ---------------------------------------------------------------------------
# Marker: fingerprint, atomic write, read, freshness predicate.
# ---------------------------------------------------------------------------


def _repo_root() -> Path:
    """Repository root — this file is ``<root>/pinn/verify.py``."""
    return Path(__file__).resolve().parents[1]


def git_head() -> tuple[Optional[str], bool]:
    """Return ``(head_sha, available)`` from a bounded ``git rev-parse HEAD``.

    A missing git binary, a non-repository directory, a non-zero exit, and a
    timeout are all reported as unavailable — verify still reports its ladder
    result; only the marker's authority is withdrawn.
    """
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(_repo_root()),
            capture_output=True,
            text=True,
            timeout=_GIT_TIMEOUT_S,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None, False
    if completed.returncode != 0:
        return None, False
    head = completed.stdout.strip()
    if not head:
        return None, False
    return head, True


def current_fingerprint(*, precision: str, device: str) -> dict[str, Any]:
    """The runtime + code fingerprint a marker must match to stay authoritative."""
    import torch

    from pinn.runtime import resolve_runtime

    try:
        spec = resolve_runtime(precision, device)
        dtype = str(spec.dtype)
        device_label = spec.torch_device.type
    except ValueError:
        # An unsupported pair still fingerprints honestly (as requested), so a
        # marker written under it can never match a supported-pair launch.
        dtype = f"unresolved:{precision}"
        device_label = device
    head, available = git_head()
    return {
        "device": device_label,
        "dtype": dtype,
        "torch_version": str(torch.__version__),
        "python_version": platform.python_version(),
        "git_head": head,
        "git_head_available": available,
    }


def marker_path(runs_root: Optional[Path] = None) -> Path:
    """Resolve the marker path and refuse anything escaping the runs root."""
    root = Path(runs_root if runs_root is not None else _RUNS_ROOT).resolve()
    path = (root / MARKER_RELATIVE_PATH).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:  # pragma: no cover — constant relative path
        raise ValueError(
            f"verify marker path escapes the runs root: {path} !< {root}"
        ) from exc
    return path


def write_verify_marker(
    results: Sequence[Mapping[str, Any]],
    *,
    precision: str,
    device: str,
    runs_root: Optional[Path] = None,
    fingerprint: Optional[Mapping[str, Any]] = None,
    now: Optional[datetime] = None,
) -> Path:
    """Atomically write ``runs/.verify/latest-marker.json`` for ANY outcome.

    A red ladder is recorded just as a green one is: the marker is the record of
    what verify observed, and the freshness predicate — not the writer — decides
    whether it may authorize a long run.
    """
    records = [
        {
            "name": str(record.get("name")),
            "passed": bool(record.get("passed")),
            "reason": record.get("reason"),
        }
        for record in results
    ]
    green = ladder_is_green(records)
    stamp = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    payload = {
        "schema_version": MARKER_SCHEMA_VERSION,
        "timestamp": stamp.isoformat(),
        "verdict": VERDICT_GREEN if green else VERDICT_RED,
        "first_failed_rung": first_failed_rung(records),
        "rungs": records,
        "fingerprint": dict(
            fingerprint
            if fingerprint is not None
            else current_fingerprint(precision=precision, device=device)
        ),
    }
    destination = marker_path(runs_root)
    return atomic_write_text(destination, json.dumps(payload, indent=2) + "\n")


def read_verify_marker(runs_root: Optional[Path] = None) -> Optional[dict[str, Any]]:
    """Read the marker, or None when it is absent/unreadable/not valid JSON."""
    path = marker_path(runs_root)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        marker = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(marker, dict):
        return None
    return marker


def marker_is_green_and_fresh(
    marker: Optional[Mapping[str, Any]],
    *,
    fingerprint: Mapping[str, Any],
    now: Optional[datetime] = None,
    max_age_s: float = DEFAULT_MAX_MARKER_AGE_S,
) -> bool:
    """Fail-closed: green verdict AND inside the window AND full fingerprint match.

    Every fingerprint value is compared, including ``git_head`` and
    ``git_head_available`` — so a green marker from *different code*, a
    different Torch/Python build, a different device/dtype, or a run whose code
    identity could not be established never authorizes a long run.
    """
    if not isinstance(marker, Mapping):
        return False
    if marker.get("schema_version") != MARKER_SCHEMA_VERSION:
        return False
    if marker.get("verdict") != VERDICT_GREEN:
        return False
    rungs = marker.get("rungs")
    if not _marker_ladder_is_valid(rungs):
        return False

    stamp = marker.get("timestamp")
    if not isinstance(stamp, str):
        return False
    try:
        written = datetime.fromisoformat(stamp)
    except ValueError:
        return False
    if written.tzinfo is None:
        return False
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    age_s = (current - written.astimezone(timezone.utc)).total_seconds()
    if age_s < 0 or age_s > float(max_age_s):
        return False

    recorded = marker.get("fingerprint")
    if not isinstance(recorded, Mapping) or not isinstance(fingerprint, Mapping):
        return False
    if not _FINGERPRINT_KEYS.issubset(recorded) or not _FINGERPRINT_KEYS.issubset(
        fingerprint
    ):
        return False
    # A marker whose code identity is unknown can never authorize a long run.
    if not recorded.get("git_head_available") or not fingerprint.get(
        "git_head_available"
    ):
        return False
    for key, expected in fingerprint.items():
        if recorded.get(key) != expected:
            return False
    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m pinn.verify",
        description=(
            "Run the ACC-01 pre-flight verification ladder (device sanity, "
            "componentwise AD, fp64-CPU gradcheck, residual-on-ground-truth, "
            "single-trajectory overfit) and write the verdict marker."
        ),
    )
    parser.add_argument(
        "--precision",
        default=DEFAULT_PRECISION,
        choices=("float32", "float64"),
        help="arm precision for rungs 1/2/4/5 (rung 3 is always float64)",
    )
    parser.add_argument(
        "--device",
        default=DEFAULT_DEVICE,
        choices=("mps", "cpu"),
        help="arm device for rungs 1/2/4/5 (rung 3 is always cpu)",
    )
    parser.add_argument(
        "--variant",
        default=DEFAULT_VARIANT,
        help="ground-truth dataset variant for rungs 4 and 5",
    )
    parser.add_argument(
        "--id",
        dest="trajectory_id",
        default=DEFAULT_TRAJECTORY_ID,
        help="ground-truth trajectory id for rungs 4 and 5",
    )
    parser.add_argument(
        "--overfit-max-steps",
        type=int,
        default=None,
        help="override the overfit probe's own max-step cap",
    )
    parser.add_argument(
        "--runs-root",
        type=Path,
        default=None,
        help="runs root under which the verdict marker is written",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """CLI entry — returns 0 only when every rung PASSed."""
    args = _parser().parse_args(list(argv) if argv is not None else None)

    results = run_ladder(
        precision=args.precision,
        device=args.device,
        variant=args.variant,
        trajectory_id=args.trajectory_id,
        overfit_max_steps=args.overfit_max_steps,
    )

    for record in results:
        verdict = "PASS" if record["passed"] else "FAIL"
        line = f"{verdict}  {record['name']}"
        if record["reason"]:
            line = f"{line} — {record['reason']}"
        print(line)

    try:
        written = write_verify_marker(
            results,
            precision=args.precision,
            device=args.device,
            runs_root=args.runs_root,
        )
        print(f"verify marker: {written}")
    except (OSError, ValueError) as exc:
        print(f"error: could not write the verify marker: {exc}", file=sys.stderr)
        return 1

    green = ladder_is_green(results)
    if green:
        print(f"VERIFY: GREEN — all {len(LADDER)} rungs PASS")
        return 0
    failed = first_failed_rung(results)
    # Flush the per-rung lines first so a terminal shows the ladder above the
    # verdict rather than interleaving the two streams.
    sys.stdout.flush()
    print(
        f"VERIFY: RED — first failed rung: {failed}",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
