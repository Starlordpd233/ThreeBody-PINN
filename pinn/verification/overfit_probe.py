"""Phase 38 rung 4: single-trajectory data-path overfit probe (NET-05).

Optimizes the DATA-Huber term through the real model + hard COM projection head
on one trajectory, driving data-loss reduction ``L0 / Lf >= 1e3``. Conditions
the model on ``tau_ic13(u) = [2u-1, zeros(13)]`` — a fixed Phase-38 placeholder
(physically-normalized IC13 is Phase 39).

Additionally evaluates input-available loss-catalog diagnostics at the initial
and final steps (data, IC, causal-physics, angular-momentum). Soft-energy is
recorded as ``not evaluated — requires Phase 39/40 metadata`` unless optional
``--eps-h`` is supplied. Non-finite input-available diagnostics FAIL loudly.
"""

from __future__ import annotations

# Capture before Torch import — Phase 37 probe grammar.
import os as _os

_PRE_IMPORT_FALLBACK = _os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") or None

import argparse
import datetime as dt
import json
import math
import sys
import warnings
from pathlib import Path

import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.constants import (
    CAUSAL_ETA_C,
    D_CHARACTERISTIC_LENGTH,
    EPS_SOFT,
    T_CHARACTERISTIC_TIME,
)
from pinn.loss_catalog import (
    angular_momentum_loss,
    causal_physics_loss,
    data_huber_loss,
    ic_anchor_loss,
    soft_energy_loss,
)
from pinn.network import build_network
from pinn.physics_residual import componentwise_du, physics_residual
from pinn.runtime import resolve_runtime
from pinn.verification.fixture_loader import load_trajectory

__all__ = ["main", "run_overfit"]

DEFAULT_MAX_STEPS = 3000
DEFAULT_LR = 1e-3
DEFAULT_COM_OFFSET_WARN = 1e-3
PASS_RATIO = 1e3
IC13_PLACEHOLDER_NOTE = (
    "zeros(13) — Phase-38 overfit smoke; physically-normalized IC13 deferred to Phase 39"
)
SOFT_ENERGY_NOT_EVALUATED = "not evaluated — requires Phase 39/40 metadata"

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_EVIDENCE_ROOT = (
    _REPO_ROOT / ".planning" / "phases" /
    "38-pinn-model-rebuild-from-specs-fut-01" / "evidence" / "overfit"
)
_N_BODIES = 3
_N_DIMS = 3


class OverfitFail(Exception):
    """Typed fail-loud exit for non-finite loss / diagnostic / cap failures."""

    def __init__(self, reason: str, **fields):
        super().__init__(reason)
        self.reason = reason
        self.fields = fields


def _reject_dataset_evidence_root(evidence_root: Path) -> None:
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
    ratio = raw.get("ratio")
    summary = (
        "# Phase 38 Rung 4: Single-Trajectory Overfit\n\n"
        f"- Result: {'PASS' if raw.get('passed') else 'FAIL'}\n"
        f"- Initial data loss L0: {raw.get('initial_loss')!r}\n"
        f"- Floor data loss Lf: {raw.get('floor_loss')!r}\n"
        f"- Ratio L0/Lf: {ratio!r} (gate >= {PASS_RATIO:g})\n"
        f"- Steps: {raw.get('steps')!r}\n"
        f"- LR: {raw.get('lr')!r}\n"
        f"- IC13 placeholder: {raw.get('ic13_placeholder')!r}\n"
        f"- Fail reason: {raw.get('fail_reason')!r}\n"
    )
    if raw.get("fail_reason") == "cap_without_target":
        summary += (
            "\nCap-reached FAIL calibration guidance: if the ratio was still "
            "improving, re-run with a larger `--max-steps` and/or a tuned `--lr`; "
            "a plateaued ratio indicates a wiring problem. The default "
            f"`--max-steps {DEFAULT_MAX_STEPS}` / `--lr {DEFAULT_LR}` are "
            "uncalibrated build-engineering knobs, not a wiring verdict.\n"
        )
    _atomic_write(run_dir / "summary.md", summary)
    (run_dir / "summary.md").chmod(0o600)
    return run_dir


def _build_tau_ic13(u: torch.Tensor, *, dtype, device) -> torch.Tensor:
    """``tau_ic13(u) = [2u-1, zeros(13)]`` — fixed Phase-38 placeholder IC13."""
    u_t = torch.as_tensor(u, dtype=dtype, device=device).reshape(-1)
    tau = torch.as_tensor(2.0, dtype=dtype, device=device) * u_t - torch.as_tensor(
        1.0, dtype=dtype, device=device
    )
    zeros = torch.zeros(u_t.shape[0], 13, dtype=dtype, device=device)
    return torch.cat([tau.unsqueeze(-1), zeros], dim=-1)


def _mass_weighted_com_offset(positions_rprime: torch.Tensor, masses: torch.Tensor) -> float:
    """Max over snapshots of |sum_i m_i r'_i| (vector norm of mass-weighted COM)."""
    com = (positions_rprime * masses.reshape(1, 3, 1)).sum(dim=1)  # (N_t, 3)
    total_mass = masses.sum()
    com = com / total_mass
    return float(torch.linalg.vector_norm(com, dim=-1).max().item())


def _matched_plummer_h0(positions_0, velocities_0, masses, *, dtype, device) -> torch.Tensor:
    """Matched-Plummer H at the t=0 snapshot (scalar)."""
    p = positions_0.reshape(_N_BODIES, _N_DIMS)
    v = velocities_0.reshape(_N_BODIES, _N_DIMS)
    m = masses.reshape(_N_BODIES)
    speed_sq = (v * v).sum(dim=-1)
    kinetic = torch.as_tensor(0.5, dtype=dtype, device=device) * (m * speed_sq).sum()
    eps = torch.as_tensor(EPS_SOFT, dtype=dtype, device=device)
    potential = torch.zeros((), dtype=dtype, device=device)
    for i in range(_N_BODIES):
        for j in range(i + 1, _N_BODIES):
            delta = p[j] - p[i]
            r_safe = torch.sqrt((delta * delta).sum() + eps * eps)
            potential = potential - (m[i] * m[j] / r_safe)
    return kinetic + potential


def _angular_momentum_l0(positions_0, velocities_0, masses, *, dtype, device) -> torch.Tensor:
    p = positions_0.reshape(_N_BODIES, _N_DIMS)
    v = velocities_0.reshape(_N_BODIES, _N_DIMS)
    m = masses.reshape(_N_BODIES)
    cross = torch.cross(p, v, dim=-1)
    return (m.unsqueeze(-1) * cross).sum(dim=0)


def _scalar_finite(value) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return False
    if torch.is_tensor(value):
        return bool(torch.isfinite(value).all())
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def _evaluate_diagnostics(
    model,
    u_points,
    true_positions_rprime,
    true_velocities_rprime,
    masses,
    *,
    eps_h,
    dtype,
    device,
):
    """Evaluate input-available loss-catalog terms (diagnostic; not optimized)."""
    tau_ic13 = _build_tau_ic13(u_points, dtype=dtype, device=device)
    pred_flat = model(tau_ic13, masses)  # (N_t, 9)
    pred_pos = pred_flat.reshape(-1, _N_BODIES, _N_DIMS)

    l_data = data_huber_loss(pred_pos, true_positions_rprime, dtype=dtype, device=device)

    # IC anchors at u=0 / first snapshot.
    u0 = u_points[:1]
    tau0 = _build_tau_ic13(u0, dtype=dtype, device=device)
    pred_r0 = model(tau0, masses).reshape(_N_BODIES, _N_DIMS)
    true_r0 = true_positions_rprime[0]
    true_v0 = true_velocities_rprime[0]

    # AD-derived velocities via PHYS-02 dr'/du path.
    def traj(u_scalar):
        t_in = _build_tau_ic13(u_scalar.reshape(()), dtype=dtype, device=device)
        return model(t_in, masses).reshape(_N_BODIES, _N_DIMS)

    first_du, _second = componentwise_du(traj, u_points)
    pred_vel = first_du.reshape(-1, _N_BODIES, _N_DIMS)
    pred_v0 = pred_vel[0]

    l_ic = ic_anchor_loss(
        pred_r0, true_r0, pred_v0, true_v0, beta_v=1.0, dtype=dtype, device=device,
    )

    # Causal physics via PHYS-02 residual on the model trajectory.
    residual = physics_residual(traj, u_points, masses, dtype=dtype, device=device)
    # Rbar_n = (1/3) sum_i ||f_i||^2
    rbar = (residual.reshape(residual.shape[0], -1) ** 2).sum(dim=-1) / torch.as_tensor(
        float(_N_BODIES), dtype=dtype, device=device
    )
    l_phys = causal_physics_loss(
        rbar, eta_c=CAUSAL_ETA_C, times=u_points, dtype=dtype, device=device,
    )

    l0 = _angular_momentum_l0(
        true_positions_rprime[0], true_velocities_rprime[0], masses,
        dtype=dtype, device=device,
    )
    l_ang = angular_momentum_loss(
        pred_pos, pred_vel, l0, masses=masses, dtype=dtype, device=device,
    )

    if eps_h is None:
        soft = SOFT_ENERGY_NOT_EVALUATED
    else:
        h0 = _matched_plummer_h0(
            true_positions_rprime[0], true_velocities_rprime[0], masses,
            dtype=dtype, device=device,
        )
        soft = soft_energy_loss(
            pred_pos, pred_vel, h0, eps_h, masses=masses, dtype=dtype, device=device,
        )

    def _to_jsonable(val):
        if isinstance(val, str):
            return val
        if torch.is_tensor(val):
            return float(val.detach().cpu())
        return float(val)

    return {
        "data": _to_jsonable(l_data),
        "ic": _to_jsonable(l_ic),
        "causal_physics": _to_jsonable(l_phys),
        "angular_momentum": _to_jsonable(l_ang),
        "soft_energy": soft if isinstance(soft, str) else _to_jsonable(soft),
    }


def _assert_diagnostics_finite(diag: dict, step_label: str) -> None:
    for term in ("data", "ic", "causal_physics", "angular_momentum"):
        if not _scalar_finite(diag[term]):
            raise OverfitFail(
                "non_finite_diagnostic",
                fail_term=f"{term}@{step_label}",
                step=step_label,
            )


def run_overfit(
    precision,
    device,
    *,
    path=None,
    variant=None,
    id=None,  # noqa: A002
    max_steps=DEFAULT_MAX_STEPS,
    lr=DEFAULT_LR,
    eps_h=None,
    com_offset_warn_threshold=DEFAULT_COM_OFFSET_WARN,
):
    """Run the data-path overfit and return a structured evidence dict."""
    runtime = resolve_runtime(precision, device)
    dtype = runtime.dtype
    torch_device = runtime.torch_device

    fixture = load_trajectory(
        path=path, variant=variant, id=id, dtype=dtype, device=torch_device,
    )
    # Dimensionless GT: r' = r/D, v' = v * (T/D) for diagnostics that need v'.
    d = torch.as_tensor(D_CHARACTERISTIC_LENGTH, dtype=dtype, device=torch_device)
    t_char = torch.as_tensor(T_CHARACTERISTIC_TIME, dtype=dtype, device=torch_device)
    true_pos = fixture.positions / d
    true_vel = fixture.velocities * (t_char / d)
    u_points = fixture.times / t_char
    masses = fixture.masses

    com_offset = _mass_weighted_com_offset(true_pos, masses)
    com_warn = com_offset > com_offset_warn_threshold
    if com_warn:
        warnings.warn(
            f"GT mass-weighted COM offset {com_offset:.3e} exceeds "
            f"--com-offset-warn-threshold {com_offset_warn_threshold:g}; "
            "the >=1e3x data-loss gate may be unreachable unless the GT is recentered",
            stacklevel=2,
        )

    model = build_network(ArchitectureSpec(), dtype=dtype, device=torch_device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    def data_loss_value():
        tau_ic13 = _build_tau_ic13(u_points, dtype=dtype, device=torch_device)
        pred = model(tau_ic13, masses).reshape(-1, _N_BODIES, _N_DIMS)
        return data_huber_loss(pred, true_pos, dtype=dtype, device=torch_device)

    # Initial diagnostics + initial data loss.
    with torch.no_grad():
        # Keep diagnostics outside the no_grad for AD terms — re-run with grad.
        pass
    model.eval()
    # Diagnostics need AD for physics/velocity; enable grad.
    initial_diag = _evaluate_diagnostics(
        model, u_points, true_pos, true_vel, masses,
        eps_h=eps_h, dtype=dtype, device=torch_device,
    )
    _assert_diagnostics_finite(initial_diag, "initial")

    model.train()
    loss0 = data_loss_value()
    if not bool(torch.isfinite(loss0).all()):
        raise OverfitFail("non_finite_data_loss", step=0)
    l0 = float(loss0.detach().cpu())
    floor = l0
    steps_run = 0

    for step in range(1, int(max_steps) + 1):
        optimizer.zero_grad(set_to_none=True)
        loss = data_loss_value()
        if not bool(torch.isfinite(loss).all()):
            raise OverfitFail("non_finite_data_loss", step=step)
        loss.backward()
        optimizer.step()
        steps_run = step
        # Measure post-update loss so the floor/ratio track the actual state.
        with torch.no_grad():
            post = data_loss_value()
        if not bool(torch.isfinite(post).all()):
            raise OverfitFail("non_finite_data_loss", step=step)
        current = float(post.detach().cpu())
        if current < floor:
            floor = current
        if l0 / max(floor, 1e-300) >= PASS_RATIO:
            break

    model.eval()
    final_diag = _evaluate_diagnostics(
        model, u_points, true_pos, true_vel, masses,
        eps_h=eps_h, dtype=dtype, device=torch_device,
    )
    _assert_diagnostics_finite(final_diag, "final")

    ratio = l0 / max(floor, 1e-300)
    passed = ratio >= PASS_RATIO
    fail_reason = None if passed else "cap_without_target"

    return {
        "schema_version": "phase38-overfit/v1",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "arm": {"precision": precision, "device": device},
        "passed": passed,
        "initial_loss": l0,
        "floor_loss": floor,
        "ratio": ratio,
        "steps": steps_run,
        "max_steps": int(max_steps),
        "lr": float(lr),
        "ic13_placeholder": IC13_PLACEHOLDER_NOTE,
        "mass_weighted_com_offset": com_offset,
        "com_offset_warn_threshold": float(com_offset_warn_threshold),
        "com_offset_warning": com_warn,
        "diagnostics": {"initial": initial_diag, "final": final_diag},
        "fail_reason": fail_reason,
        "provenance": fixture.provenance,
        "pre_import_fallback": _PRE_IMPORT_FALLBACK,
        "torch_build": {
            "version": torch.__version__,
            "git_version": getattr(torch.version, "git_version", None),
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m pinn.verification.overfit_probe",
        description="Run the Phase 38 single-trajectory overfit probe (rung 4).",
    )
    parser.add_argument("--precision", required=True, choices=("float32", "float64"))
    parser.add_argument("--device", required=True, choices=("mps", "cpu"))
    parser.add_argument("--path", type=Path)
    parser.add_argument("--variant")
    parser.add_argument("--id")
    parser.add_argument("--max-steps", type=int, default=DEFAULT_MAX_STEPS)
    parser.add_argument("--lr", type=float, default=DEFAULT_LR)
    parser.add_argument(
        "--eps-h",
        type=float,
        default=None,
        help="Optional diagnostic soft-energy metadata floor (1e-4*S_H). "
             "When omitted, soft-energy is recorded as not evaluated.",
    )
    parser.add_argument(
        "--com-offset-warn-threshold",
        type=float,
        default=DEFAULT_COM_OFFSET_WARN,
    )
    parser.add_argument("--evidence-root", type=Path, default=_DEFAULT_EVIDENCE_ROOT)
    args = parser.parse_args(argv)

    by_path = args.path is not None
    by_variant = args.variant is not None or args.id is not None
    if by_path == by_variant or (by_variant and (args.variant is None or args.id is None)):
        parser.error("provide exactly one trajectory form: --path OR --variant together with --id")
    if args.max_steps < 1:
        parser.error("--max-steps must be >= 1")
    if args.lr <= 0:
        parser.error("--lr must be positive")

    raw = {
        "schema_version": "phase38-overfit/v1",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "arm": {"precision": args.precision, "device": args.device},
        "passed": False,
        "initial_loss": None,
        "floor_loss": None,
        "ratio": None,
        "steps": None,
        "max_steps": args.max_steps,
        "lr": args.lr,
        "ic13_placeholder": IC13_PLACEHOLDER_NOTE,
        "mass_weighted_com_offset": None,
        "com_offset_warn_threshold": args.com_offset_warn_threshold,
        "com_offset_warning": False,
        "diagnostics": None,
        "fail_reason": None,
        "provenance": None,
        "pre_import_fallback": _PRE_IMPORT_FALLBACK,
        "torch_build": {
            "version": torch.__version__,
            "git_version": getattr(torch.version, "git_version", None),
        },
    }
    try:
        raw = run_overfit(
            args.precision,
            args.device,
            path=args.path,
            variant=args.variant,
            id=args.id,
            max_steps=args.max_steps,
            lr=args.lr,
            eps_h=args.eps_h,
            com_offset_warn_threshold=args.com_offset_warn_threshold,
        )
    except OverfitFail as exc:
        raw["fail_reason"] = exc.reason
        raw["passed"] = False
        for key, value in exc.fields.items():
            raw[key] = value
    except Exception as exc:  # noqa: BLE001 — retain structured failure evidence
        raw["fail_reason"] = "exception"
        raw["exception"] = {"type": type(exc).__name__, "message": str(exc)}
        raw["passed"] = False

    run_dir = _write_evidence(raw, args.evidence_root)
    ratio = raw.get("ratio")
    verdict = "PASS" if raw.get("passed") else "FAIL"
    print(
        f"Overfit data-loss L0={raw.get('initial_loss')!r} Lf={raw.get('floor_loss')!r} "
        f"ratio={ratio!r} (gate>={PASS_RATIO:g}) steps={raw.get('steps')!r} "
        f"lr={raw.get('lr')!r}; {verdict}; evidence={run_dir}"
    )
    if raw.get("fail_reason"):
        print(f"fail_reason={raw['fail_reason']!r}")
    return 0 if raw.get("passed") else 1


if __name__ == "__main__":
    sys.exit(main())
