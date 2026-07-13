"""Phase 38 rung 3: dual-gate residual evidence on one Brutus trajectory.

Gate A checks the direct §3.2 softened force against the negative autograd
gradient of the §3.4 matched-Plummer potential. Gate B independently compares
that force with the trajectory's finite-differenced acceleration on the
dimensionless ``u = t / T`` leaf. A run passes only when both gates pass.
"""

from __future__ import annotations

# This must precede Torch and pinn.runtime imports: it is the only reliable
# record of the fallback environment that existed before Torch initialization.
import os as _os

_PRE_IMPORT_FALLBACK = _os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") or None

import argparse
import datetime as dt
import json
from pathlib import Path
import sys

import torch

from pinn.constants import D_CHARACTERISTIC_LENGTH, EPS_SOFT, T_CHARACTERISTIC_TIME
from pinn.physics_residual import softened_acceleration
from pinn.runtime import resolve_runtime
from pinn.verification.fixture_loader import load_trajectory


DEFAULT_RESIDUAL_THRESHOLD = 1e-5
DEFAULT_NEWTONIAN_RESIDUAL_THRESHOLD = 1e-1
DEFAULT_MIN_SEPARATION_GUARD = 1e-3
_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_EVIDENCE_ROOT = (
    _REPO_ROOT / ".planning" / "phases" /
    "38-pinn-model-rebuild-from-specs-fut-01" / "evidence" / "residual"
)

__all__ = ["main", "run_residual_on_ground_truth"]


def _reject_dataset_evidence_root(evidence_root: Path) -> None:
    """Prevent an untrusted evidence-root from writing into simulation_data."""
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
    """Allocate a non-overwriting UTC run directory, including same-second runs."""
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
        "# Phase 38 Rung 3: Residual on Ground Truth\n\n"
        f"- Gate A: {'PASS' if raw['gate_a']['passed'] else 'FAIL'} "
        f"(max relative error {raw['gate_a']['max_relative_error']!r}; "
        f"threshold {raw['thresholds']['force_energy_relative_error']})\n"
        f"- Gate B: {'PASS' if raw['gate_b']['passed'] else 'FAIL'} "
        f"(median relative error {raw['gate_b']['median_relative_error']!r}; "
        f"threshold {raw['thresholds']['newtonian_median_relative_error']})\n"
        f"- Excluded snapshots: {raw['excluded_snapshot_count']}\n"
        f"- GT mass-weighted COM offset: {raw['mass_weighted_com_offset']!r}\n"
        f"- Overall: {'PASS' if raw['passed'] else 'FAIL'}\n"
    )
    _atomic_write(run_dir / "summary.md", summary)
    (run_dir / "summary.md").chmod(0o600)
    return run_dir


def _minimum_pairwise_separation(positions: torch.Tensor) -> torch.Tensor:
    """Return the minimum off-diagonal separation per snapshot in r' units."""
    difference = positions.unsqueeze(-3) - positions.unsqueeze(-2)
    separation = torch.linalg.vector_norm(difference, dim=-1)
    eye = torch.eye(3, dtype=torch.bool, device=positions.device)
    separation = separation.masked_fill(eye, torch.inf)
    return separation.amin(dim=(-2, -1))


def _gate_a_autograd(positions: torch.Tensor, masses: torch.Tensor,
                     qualifying: torch.Tensor, threshold: float, *, dtype, device) -> dict:
    """Compare autograd(-grad V_eps)/m with the direct softened acceleration."""
    if not bool(qualifying.any()):
        return {"passed": False, "max_relative_error": None, "per_body_relative_error": []}

    position_leaves = positions[qualifying].detach().clone().requires_grad_(True)
    V_eps = position_leaves.new_zeros(())
    for body_i in range(3):
        for body_j in range(body_i + 1, 3):
            delta = position_leaves[:, body_j] - position_leaves[:, body_i]
            safe_distance = torch.sqrt((delta * delta).sum(dim=-1) + EPS_SOFT * EPS_SOFT)
            V_eps = V_eps - (masses[body_i] * masses[body_j] / safe_distance).sum()

    gradient = torch.autograd.grad(V_eps, position_leaves)[0]
    implied_acceleration = -gradient / masses.reshape(1, 3, 1)
    direct_acceleration = softened_acceleration(
        position_leaves,
        masses,
        dtype=dtype,
        device=device,
    )
    difference = torch.linalg.vector_norm(implied_acceleration - direct_acceleration, dim=-1)
    denominator = torch.linalg.vector_norm(direct_acceleration, dim=-1).clamp_min(1e-12)
    relative_error = difference / denominator
    maximum = float(relative_error.max().item())
    return {
        "passed": bool(torch.all(relative_error < threshold)),
        "max_relative_error": maximum,
        "per_body_relative_error": relative_error.detach().cpu().tolist(),
    }


def _u_leaf_acceleration(velocities_raw: torch.Tensor, times_raw: torch.Tensor) -> torch.Tensor:
    """Central-difference v'=v_raw*(T/D) on u=t/T, one-sided at endpoints."""
    u = times_raw / T_CHARACTERISTIC_TIME
    velocity_physics = velocities_raw * (T_CHARACTERISTIC_TIME / D_CHARACTERISTIC_LENGTH)
    if u.numel() < 2:
        raise ValueError("residual probe needs at least two trajectory snapshots")
    acceleration = torch.empty_like(velocity_physics)
    acceleration[0] = (velocity_physics[1] - velocity_physics[0]) / (u[1] - u[0])
    acceleration[-1] = (velocity_physics[-1] - velocity_physics[-2]) / (u[-1] - u[-2])
    if u.numel() > 2:
        denominator = (u[2:] - u[:-2]).reshape(-1, 1, 1)
        acceleration[1:-1] = (velocity_physics[2:] - velocity_physics[:-2]) / denominator
    return acceleration


def _gate_b_ground_truth(positions: torch.Tensor, velocities_raw: torch.Tensor,
                         times_raw: torch.Tensor, masses: torch.Tensor,
                         qualifying: torch.Tensor, threshold: float, *, dtype, device) -> dict:
    """Compare u-leaf finite-difference acceleration to the softened force sum."""
    if not bool(qualifying.any()):
        return {"passed": False, "median_relative_error": None, "max_relative_error": None}

    finite_difference_acceleration = _u_leaf_acceleration(velocities_raw, times_raw)
    force_acceleration = softened_acceleration(positions, masses, dtype=dtype, device=device)
    residual = finite_difference_acceleration - force_acceleration
    residual_norm = torch.linalg.vector_norm(residual.reshape(residual.shape[0], -1), dim=-1)
    acceleration_norm = torch.linalg.vector_norm(
        finite_difference_acceleration.reshape(finite_difference_acceleration.shape[0], -1), dim=-1
    ).clamp_min(1e-12)
    relative_error = residual_norm / acceleration_norm
    qualifying_error = relative_error[qualifying]
    median = float(torch.median(qualifying_error).item())
    maximum = float(torch.max(qualifying_error).item())
    return {
        "passed": median < threshold,
        "median_relative_error": median,
        "max_relative_error": maximum,
    }


def run_residual_on_ground_truth(precision, device, *, path=None, variant=None, id=None,
                                 residual_threshold=DEFAULT_RESIDUAL_THRESHOLD,
                                 newtonian_residual_threshold=DEFAULT_NEWTONIAN_RESIDUAL_THRESHOLD,
                                 min_separation_guard=DEFAULT_MIN_SEPARATION_GUARD):
    """Run both gates on one read-only Brutus fixture and return measured evidence."""
    runtime = resolve_runtime(precision, device)
    dtype = runtime.dtype
    torch_device = runtime.torch_device
    fixture = load_trajectory(
        path=path,
        variant=variant,
        id=id,
        dtype=dtype,
        device=torch_device,
    )
    positions = fixture.positions / D_CHARACTERISTIC_LENGTH
    minimum_separation = _minimum_pairwise_separation(positions)
    qualifying = minimum_separation >= min_separation_guard
    excluded_snapshot_count = int((~qualifying).sum().item())
    gate_a = _gate_a_autograd(
        positions, fixture.masses, qualifying, residual_threshold, dtype=dtype, device=torch_device
    )
    gate_b = _gate_b_ground_truth(
        positions,
        fixture.velocities,
        fixture.times,
        fixture.masses,
        qualifying,
        newtonian_residual_threshold,
        dtype=dtype,
        device=torch_device,
    )
    com_offset = torch.linalg.vector_norm(
        (positions * fixture.masses.reshape(1, 3, 1)).sum(dim=1), dim=-1
    ).max()
    return {
        "schema_version": "phase38-residual/v1",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "arm": {"precision": precision, "device": device},
        "thresholds": {
            "force_energy_relative_error": residual_threshold,
            "newtonian_median_relative_error": newtonian_residual_threshold,
            "min_separation_guard": min_separation_guard,
        },
        "gate_a": gate_a,
        "gate_b": gate_b,
        "excluded_snapshot_count": excluded_snapshot_count,
        "mass_weighted_com_offset": float(com_offset.item()),
        "provenance": fixture.provenance,
        "finite_difference": {
            "time_leaf": "u = t/T",
            "velocity_map": "v_raw * (T/D)",
            "scheme": "central; one-sided endpoints",
        },
        "pre_import_fallback": _PRE_IMPORT_FALLBACK,
        "torch_build": {
            "version": torch.__version__,
            "git_version": getattr(torch.version, "git_version", None),
        },
        "passed": gate_a["passed"] and gate_b["passed"],
    }


def _failed_record(args, exception: Exception) -> dict:
    """Retain a structured failed invocation instead of swallowing its cause."""
    return {
        "schema_version": "phase38-residual/v1",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "arm": {"precision": args.precision, "device": args.device},
        "thresholds": {
            "force_energy_relative_error": args.residual_threshold,
            "newtonian_median_relative_error": args.newtonian_residual_threshold,
            "min_separation_guard": args.min_separation_guard,
        },
        "gate_a": {"passed": False, "max_relative_error": None, "per_body_relative_error": []},
        "gate_b": {"passed": False, "median_relative_error": None, "max_relative_error": None},
        "excluded_snapshot_count": 0,
        "mass_weighted_com_offset": None,
        "provenance": None,
        "finite_difference": {
            "time_leaf": "u = t/T",
            "velocity_map": "v_raw * (T/D)",
            "scheme": "central; one-sided endpoints",
        },
        "pre_import_fallback": _PRE_IMPORT_FALLBACK,
        "torch_build": {"version": torch.__version__, "git_version": getattr(torch.version, "git_version", None)},
        "exception": {"type": type(exception).__name__, "message": str(exception)},
        "passed": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m pinn.verification.residual_probe",
        description="Run the Phase 38 dual-gate residual probe on one Brutus trajectory.",
    )
    parser.add_argument("--precision", required=True, choices=("float32", "float64"))
    parser.add_argument("--device", required=True, choices=("mps", "cpu"))
    parser.add_argument("--path", type=Path)
    parser.add_argument("--variant")
    parser.add_argument("--id")
    parser.add_argument("--residual-threshold", type=float, default=DEFAULT_RESIDUAL_THRESHOLD)
    parser.add_argument(
        "--newtonian-residual-threshold",
        type=float,
        default=DEFAULT_NEWTONIAN_RESIDUAL_THRESHOLD,
    )
    parser.add_argument("--min-separation-guard", type=float, default=DEFAULT_MIN_SEPARATION_GUARD)
    parser.add_argument("--evidence-root", type=Path, default=_DEFAULT_EVIDENCE_ROOT)
    args = parser.parse_args(argv)

    by_path = args.path is not None
    by_variant = args.variant is not None or args.id is not None
    if by_path == by_variant or (by_variant and (args.variant is None or args.id is None)):
        parser.error("provide exactly one trajectory form: --path OR --variant together with --id")
    if args.residual_threshold <= 0 or args.newtonian_residual_threshold <= 0:
        parser.error("residual thresholds must be positive")
    if args.min_separation_guard < 0:
        parser.error("min-separation-guard must be non-negative")

    try:
        raw = run_residual_on_ground_truth(
            args.precision,
            args.device,
            path=args.path,
            variant=args.variant,
            id=args.id,
            residual_threshold=args.residual_threshold,
            newtonian_residual_threshold=args.newtonian_residual_threshold,
            min_separation_guard=args.min_separation_guard,
        )
    except Exception as exc:  # noqa: BLE001 - fail evidence must preserve loader/runtime errors
        raw = _failed_record(args, exc)
    run_dir = _write_evidence(raw, args.evidence_root)
    print(
        "Gate A force-energy: "
        f"{raw['gate_a']['max_relative_error']!r} < {args.residual_threshold:g}; "
        f"{'PASS' if raw['gate_a']['passed'] else 'FAIL'}"
    )
    print(
        "Gate B u-leaf Newtonian median: "
        f"{raw['gate_b']['median_relative_error']!r} < {args.newtonian_residual_threshold:g}; "
        f"{'PASS' if raw['gate_b']['passed'] else 'FAIL'}"
    )
    print(f"Residual probe {'PASS' if raw['passed'] else 'FAIL'}; evidence={run_dir}")
    return 0 if raw["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
