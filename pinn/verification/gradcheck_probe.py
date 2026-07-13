"""Phase 38 rung 2: fp64-CPU gradcheck of the PHYS-02 residual.

This module deliberately requires an explicit precision/device arm. Gradcheck
is a finite-difference oracle, so it is certified only on the explicit
``float64``/``cpu`` runtime profile; another valid arm is recorded as a FAIL
rather than silently redirected or defaulted.
"""

from __future__ import annotations

# Capture this before importing Torch. Torch reads the fallback setting while
# importing, so evidence must retain the fact that existed before that point.
import os as _os

_PRE_IMPORT_FALLBACK = _os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") or None

import argparse
import datetime as dt
import json
from pathlib import Path
import sys

import torch

from pinn.physics_residual import physics_residual
from pinn.runtime import resolve_runtime


GRADCHECK_EPS = 1e-6
GRADCHECK_ATOL = 1e-5
GRADCHECK_RTOL = 1e-3
_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_EVIDENCE_ROOT = (
    _REPO_ROOT / ".planning" / "phases" /
    "38-pinn-model-rebuild-from-specs-fut-01" / "evidence" / "gradcheck"
)

__all__ = ["main", "run_gradcheck"]


def _reject_dataset_evidence_root(evidence_root: Path) -> None:
    """Keep an untrusted evidence-root argument from targeting simulation_data."""
    dataset_root = (_REPO_ROOT / "simulation_data").resolve()
    try:
        evidence_root.resolve().relative_to(dataset_root)
    except ValueError:
        return
    raise ValueError("evidence-root must not be inside simulation_data")


def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + f".tmp.{_os.getpid()}")
    with open(temporary, "w", encoding="utf-8") as handle:
        handle.write(content)
        handle.flush()
        _os.fsync(handle.fileno())
    _os.replace(temporary, path)


def _new_run_dir(evidence_root: Path) -> Path:
    """Create an exclusive UTC evidence directory without overwriting a run."""
    _reject_dataset_evidence_root(evidence_root)
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for suffix in range(1000):
        name = run_id if suffix == 0 else f"{run_id}-{suffix:03d}"
        candidate = evidence_root / name
        try:
            candidate.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            continue
        return candidate
    raise FileExistsError(f"could not allocate exclusive evidence directory under {evidence_root}")


def _write_evidence(raw: dict, evidence_root: Path) -> Path:
    run_dir = _new_run_dir(evidence_root)
    _atomic_write(run_dir / "raw.json", json.dumps(raw, sort_keys=True, indent=2) + "\n")
    summary = (
        "# Phase 38 Rung 2: Gradcheck\n\n"
        f"- Arm: `{raw['arm']['precision']}` / `{raw['arm']['device']}`\n"
        f"- Tolerances: eps={raw['tolerances']['eps']}, "
        f"atol={raw['tolerances']['atol']}, rtol={raw['tolerances']['rtol']}\n"
        f"- Result: {'PASS' if raw['gradcheck_result'] else 'FAIL'}\n"
        f"- Pre-import MPS fallback: {raw['pre_import_fallback']!r}\n"
    )
    _atomic_write(run_dir / "summary.md", summary)
    (run_dir / "summary.md").chmod(0o600)
    return run_dir


def run_gradcheck(precision, device):
    """Run residual gradcheck on a well-separated fp64-CPU synthetic closure."""
    runtime = resolve_runtime(precision, device)
    if (precision, device) != ("float64", "cpu"):
        return {
            "passed": False,
            "reason": "gradcheck requires the explicit fp64-CPU arm",
            "runtime": runtime,
            "exception": None,
        }

    dtype = runtime.dtype
    torch_device = runtime.torch_device
    masses = torch.tensor([1.0, 1.1, 0.9], dtype=dtype, device=torch_device)
    velocity = torch.tensor(
        [[0.15, -0.08, 0.03], [-0.04, 0.11, -0.02], [0.06, 0.01, -0.05]],
        dtype=dtype,
        device=torch_device,
    )
    acceleration = torch.tensor(
        [[0.02, -0.01, 0.00], [-0.01, 0.03, 0.01], [0.00, -0.02, -0.01]],
        dtype=dtype,
        device=torch_device,
    )
    u = torch.tensor(0.37, dtype=dtype, device=torch_device)
    positions = torch.tensor(
        [[-1.6, 0.1, 0.0], [1.3, -0.2, 0.1], [0.2, 1.8, -0.1]],
        dtype=dtype,
        device=torch_device,
        requires_grad=True,
    )

    def residual_closure(base_positions):
        def trajectory(u_leaf):
            return base_positions + velocity * u_leaf + 0.5 * acceleration * u_leaf * u_leaf

        return physics_residual(
            trajectory,
            u,
            masses,
            dtype=dtype,
            device=torch_device,
        )

    try:
        passed = bool(torch.autograd.gradcheck(
            residual_closure,
            (positions,),
            eps=GRADCHECK_EPS,
            atol=GRADCHECK_ATOL,
            rtol=GRADCHECK_RTOL,
        ))
        exception = None
    except Exception as exc:  # pragma: no cover - exercised by the CLI failure path
        passed = False
        exception = {"type": type(exc).__name__, "message": str(exc)}
    return {
        "passed": passed,
        "reason": None if passed else "torch.autograd.gradcheck returned FAIL",
        "runtime": runtime,
        "exception": exception,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m pinn.verification.gradcheck_probe",
        description="Run the Phase 38 fp64-CPU residual gradcheck probe.",
    )
    parser.add_argument("--precision", required=True, choices=("float32", "float64"))
    parser.add_argument("--device", required=True, choices=("mps", "cpu"))
    parser.add_argument("--evidence-root", type=Path, default=_DEFAULT_EVIDENCE_ROOT)
    args = parser.parse_args(argv)

    result = run_gradcheck(args.precision, args.device)
    raw = {
        "schema_version": "phase38-gradcheck/v1",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "arm": {"precision": args.precision, "device": args.device},
        "tolerances": {"eps": GRADCHECK_EPS, "atol": GRADCHECK_ATOL, "rtol": GRADCHECK_RTOL},
        "gradcheck_result": result["passed"],
        "reason": result["reason"],
        "exception": result["exception"],
        "pre_import_fallback": _PRE_IMPORT_FALLBACK,
        "torch_build": {
            "version": torch.__version__,
            "git_version": getattr(torch.version, "git_version", None),
        },
    }
    run_dir = _write_evidence(raw, args.evidence_root)
    criterion = f"eps={GRADCHECK_EPS:g}, atol={GRADCHECK_ATOL:g}, rtol={GRADCHECK_RTOL:g}"
    verdict = "PASS" if result["passed"] else "FAIL"
    print(f"Gradcheck fp64-CPU tolerances: {criterion}; {verdict}; evidence={run_dir}")
    if result["reason"]:
        print(result["reason"])
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
